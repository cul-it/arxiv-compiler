"""
Content store for compiled representation of paper.

Uses S3 as the underlying storage facility.
"""

import json
from typing import Tuple, Optional, Dict, Union, List, Any, Mapping
from functools import wraps
from hashlib import md5
from base64 import b64encode
from collections import defaultdict
import boto3
import botocore
from botocore.config import Config
from botocore.exceptions import ClientError
from flask import Flask

from arxiv.base import logging
from arxiv.base.globals import get_application_global, get_application_config

from ...domain import Task, Product, Format


logger = logging.getLogger(__name__)


class DoesNotExist(Exception):
    """The requested content does not exist."""


class NoSuchBucket(Exception):
    """The configured bucket does not exist."""


def hash_content(body: bytes) -> str:
    """Generate an encoded MD5 hash of a bytes."""
    return b64encode(md5(body).digest()).decode('utf-8')


class Store:
    """Represents an object store session."""

    LOG_KEY = '{src_id}/{chk}/{out_fmt}/{src_id}.{ext}.log'
    KEY = '{src_id}/{chk}/{out_fmt}/{src_id}.{ext}'

    def __init__(self, bucket: str, verify: bool = False,
                 region_name: Optional[str] = None,
                 endpoint_url: Optional[str] = None,
                 aws_access_key_id: Optional[str] = None,
                 aws_secret_access_key: Optional[str] = None) -> None:
        """Initialize with connection config parameters."""
        self._bucket = bucket
        self._region_name = region_name
        self._endpoint_url = endpoint_url
        self._verify = verify
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self.client = self._new_client()

    def _new_client(self, config: Optional[Config] = None) -> boto3.client:
        # Only add credentials to the client if they are explicitly set.
        # If they are not set, boto3 falls back to environment variables and
        # credentials files.
        params: Dict[str, Any] = {'region_name': self._region_name}
        if self._aws_access_key_id and self._aws_secret_access_key:
            params['aws_access_key_id'] = self._aws_access_key_id
            params['aws_secret_access_key'] = self._aws_secret_access_key
        if self._endpoint_url:
            params['endpoint_url'] = self._endpoint_url
            params['verify'] = self._verify
        logger.debug('new client with params %s', params)
        return boto3.client('s3', **params)

    def _handle_client_error(self, exc: ClientError) -> None:
        logger.error('error: %s', str(exc.response))
        if exc.response['Error']['Code'] == 'NoSuchBucket':
            logger.error('Caught ClientError: NoSuchBucket')
            raise NoSuchBucket(f'{self._bucket} does not exist') from exc
        if exc.response['Error']['Code'] == "NoSuchKey":
            raise DoesNotExist(f'No such object in {self._bucket}') from exc
        logger.error('Unhandled ClientError: %s', exc)
        raise RuntimeError('Unhandled ClientError') from exc

    def __hash__(self) -> int:
        """Generate a unique hash for this store session using its config."""
        return hash((self._bucket, self._region_name, self._endpoint_url,
                     self._verify, self._aws_access_key_id,
                     self._aws_secret_access_key))

    def is_available(self, retries: int = 0, read_timeout: int = 5,
                     connect_timeout: int = 5) -> bool:
        """Check whether we can write to the S3 bucket."""
        try:
            self._test_put(retries=retries, read_timeout=read_timeout,
                           connect_timeout=connect_timeout)
            logger.debug('S3 is available')
            return True
        except RuntimeError:
            logger.debug('S3 is not available')
            return False

    def _test_put(self, retries: int = 0, read_timeout: int = 5,
                  connect_timeout: int = 5) -> None:
        """Test the connection to S3 by putting a tiny object."""
        # Use a new client with a short timeout and no retries by default; we
        # want to fail fast here.
        config = Config(retries={'max_attempts': retries},
                        read_timeout=read_timeout,
                        connect_timeout=connect_timeout)
        client = self._new_client(config=config)
        try:
            logger.info('trying to put to bucket %s', self._bucket)
            client.put_object(Body=b'test', Bucket=self._bucket, Key='stat')
        except ClientError as e:
            logger.error('Error when calling store: %s', e)
            self._handle_client_error(e)

    def _wait_for_bucket(self, retries: int = 0, delay: int = 0) -> None:
        """Wait for the bucket to available."""
        try:
            waiter = self.client.get_waiter('bucket_exists')
            waiter.wait(
                Bucket=self._bucket,
                WaiterConfig={
                    'Delay': delay,
                    'MaxAttempts': retries
                }
            )
        except ClientError as exc:
            self._handle_client_error(exc)

    def initialize(self) -> None:
        """Perform initial checks, e.g. at application start-up."""
        logger.info('initialize storage service')
        try:
            # We keep these tries short, since start-up connection problems
            # usually clear out pretty fast.
            if self.is_available(retries=20, connect_timeout=1,
                                 read_timeout=1):
                logger.info('storage service is already available')
                return
        except NoSuchBucket:
            logger.info('bucket does not exist; creating')
            self._create_bucket(retries=5, read_timeout=5, connect_timeout=5)
            logger.info('wait for bucket to be available')
            self._wait_for_bucket(retries=5, delay=5)
            return
        raise RuntimeError('Failed to initialize storage service')

    def store(self, product: Product, task: Task) -> None:
        """
        Store a compilation product.

        Parameters
        ----------
        product : :class:`Product`

        """
        if task.output_format is None:
            raise TypeError('Output format must not be None')

        k = self.KEY.format(src_id=task.source_id,
                            chk=task.checksum,
                            out_fmt=task.output_format.value,
                            ext=task.output_format.ext)
        self._put(k, product.stream.read(), task.content_type)

    def retrieve(self, src_id: str, chk: str, out_fmt: Format) -> Product:
        """
        Retrieve a compilation product.

        Parameters
        ----------
        src_id : str
        chk : str
        out_fmt : enum
            One of :attr:`Format`.

        Returns
        -------
        :class:`Product`

        """
        key = self.KEY.format(src_id=src_id, chk=chk, out_fmt=out_fmt.value,
                              ext=out_fmt.ext)
        resp = self._get(key)
        return Product(stream=resp['Body'], checksum=resp['ETag'][1:-1])

    def store_log(self, product: Product, task: Task) -> None:
        """
        Store a compilation log.

        Parameters
        ----------
        product : :class:`Product`
            Stream should be log content.

        """
        if task.output_format is None:
            raise TypeError('Output format must not be None')
        key = self.LOG_KEY.format(src_id=task.source_id,
                                  chk=task.checksum,
                                  out_fmt=task.output_format.value,
                                  ext=task.output_format.ext)
        log_bytes = product.stream.read()
        logger.debug('Storing %s bytes of log', len(log_bytes))
        self._put(key, log_bytes, 'text/plain')

    def retrieve_log(self, src_id: str, chk: str, out_fmt: Format) -> Product:
        """
        Retrieve a compilation log.

        Parameters
        ----------
        src_id : str
        chk : str
        out_fmt : enum
            One of :attr:`Format`.

        Returns
        -------
        :class:`Product`

        """
        key = self.LOG_KEY.format(src_id=src_id, chk=chk,
                                  out_fmt=out_fmt.value, ext=out_fmt.ext)
        resp = self._get(key)
        return Product(stream=resp['Body'], checksum=resp['ETag'][1:-1])

    def _create_bucket(self, retries: int = 2, read_timeout: int = 5,
                       connect_timeout: int = 5) -> None:
        """Create S3 bucket."""
        config = Config(retries={'max_attempts': retries},
                        read_timeout=read_timeout,
                        connect_timeout=connect_timeout)
        client = self._new_client(config=config)
        client.create_bucket(Bucket=self._bucket)

    def _get(self, key: str) -> dict:
        resp: dict
        try:
            resp = self.client.get_object(Bucket=self._bucket, Key=key)
        except ClientError as e:
            self._handle_client_error(e)
        return resp

    def _put(self, key: str, body: bytes, content_type: str) -> None:
        try:
            self.client.put_object(Body=body, Bucket=self._bucket,
                                   ContentMD5=hash_content(body),
                                   ContentType=content_type, Key=key)
        except ClientError as exc:
            self._handle_client_error(exc)

    @classmethod
    def init_app(cls, app: Flask) -> None:
        """Set defaults for required configuration parameters."""
        app.config.setdefault('AWS_REGION', 'us-east-1')
        app.config.setdefault('AWS_ACCESS_KEY_ID', None)
        app.config.setdefault('AWS_SECRET_ACCESS_KEY', None)
        app.config.setdefault('S3_ENDPOINT', None)
        app.config.setdefault('S3_VERIFY', True)
        app.config.setdefault('S3_BUCKET', 'arxiv-compiler')

    @classmethod
    def get_session(cls) -> 'Store':
        """Create a new :class:`botocore.client.S3` session."""
        config = get_application_config()
        return cls(config['S3_BUCKET'],
                   config['S3_VERIFY'],
                   config['AWS_REGION'],
                   config['S3_ENDPOINT'],
                   config['AWS_ACCESS_KEY_ID'],
                   config['AWS_SECRET_ACCESS_KEY'])

    @classmethod
    def current_session(cls) -> 'Store':
        """Get the current store session for this application."""
        g = get_application_global()
        if g is None:
            return cls.get_session()
        if 'store' not in g:
            g.store = cls.get_session()
        store: Store = g.store
        return store
