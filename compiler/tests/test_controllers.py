"""Tests for :mod:`compiler.controllers`."""

from unittest import TestCase, mock
import io
from http import HTTPStatus as status

from flask import Flask
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import NotFound, BadRequest

from ..domain import Task, Product, Format, Status
from .. import controllers, compiler
from ..services import store, filemanager


def mock_url_for(endpoint, **kwargs):
    """Simple mock for :func:`flask.url_for`."""
    params = '/'.join(map(str, kwargs.values()))
    return f'http://{endpoint}/{params}'


def raise_store_does_not_exist(*args, **kwargs):
    raise store.DoesNotExist('Nope!')


def raise_no_such_task(*args, **kwargs):
    raise compiler.NoSuchTask('Nope!')


class TestRequestCompilation(TestCase):
    """Tests for :func:`controllers.compile`."""

    def setUp(self):
        """Create an app."""
        self.app = Flask(__name__)
        filemanager.FileManager.init_app(self.app)

    def test_request_missing_parameter(self):
        """Request for a new compilation with missing parameter."""
        with self.assertRaises(BadRequest):
            controllers.compile(
                MultiDict({'checksum': 'as12345'}),
                'footoken',
                mock.MagicMock()
            )

        with self.assertRaises(BadRequest):
            controllers.compile(
                MultiDict({'source_id': '1234'}),
                'footoken',
                mock.MagicMock()
            )

    def test_bad_checksum(self):
        """Request for a new compilation with a bad checksum value."""
        request_params = MultiDict({
            'source_id': '1234',
            'checksum': 'as12345!@#$',
            'output_format': 'pdf'
        })
        with self.assertRaises(BadRequest):
            controllers.compile(request_params, 'footoken', mock.MagicMock())

    def test_bad_source_id(self):
        """Request for a new compilation with a bad source_id value."""
        request_params = MultiDict({
            'source_id': '1234!@#$',
            'checksum': 'as12345=',
            'output_format': 'pdf'
        })
        with self.assertRaises(BadRequest):
            controllers.compile(request_params, 'footoken', mock.MagicMock())

    def test_bad_format(self):
        """Request for a new compilation with a bad output_format value."""
        request_params = MultiDict({
            'source_id': '1234',
            'checksum': 'as12345=',
            'output_format': 'fdp'
        })
        with self.assertRaises(BadRequest):
            controllers.compile(request_params, 'footoken', mock.MagicMock())

    @mock.patch(f'{controllers.__name__}.url_for', mock_url_for)
    @mock.patch(f'{controllers.__name__}.compiler')
    @mock.patch(f'{controllers.__name__}.Store')
    @mock.patch(f'{controllers.__name__}.filemanager.FileManager')
    def test_compile_de_novo(self, mock_fm, mock_store, mock_compiler):
        """Request for a new compilation."""
        mock_fm.current_session.return_value.owner.return_value = None
        mock_compiler.NoSuchTask = compiler.NoSuchTask
        mock_compiler.get_task.side_effect = compiler.NoSuchTask
        task_id = '123::asdf12345zxcv::pdf'
        token = 'footoken'
        mock_compiler.start_compilation.return_value = task_id

        request_data = MultiDict({
            'source_id': '1234',
            'checksum': 'asdf12345zxcv',
            'output_format': 'pdf'
        })
        with self.app.app_context():
            response_data = controllers.compile(
                request_data,
                token,
                mock.MagicMock()
            )
        data, code, headers = response_data
        self.assertEqual(code, status.ACCEPTED)
        self.assertIn('Location', headers)
        self.assertIn(str(request_data['source_id']), headers['Location'])
        self.assertIn(request_data['checksum'], headers['Location'])
        self.assertIn(request_data['output_format'], headers['Location'])

    @mock.patch(f'{controllers.__name__}.url_for', mock_url_for)
    @mock.patch(f'{controllers.__name__}.compiler')
    @mock.patch(f'{controllers.__name__}.Store')
    def test_compile_exists(self, mock_store, mock_compiler):
        """Request for a compilation that already exists."""
        task_id = '123::asdf12345zxcv::pdf'
        source_id = '1234'
        checksum = 'asdf12345zxcv'
        output_format = 'pdf'
        token = "footoken"
        mock_compiler.get_task.return_value \
            = Task(source_id=source_id,
                   output_format=Format.PDF,
                   status=Status.COMPLETED,
                   task_id=task_id,
                   checksum=checksum)
        request_data = MultiDict({'source_id': source_id, 'checksum': checksum,
                                  'output_format': output_format})
        mock_session = mock.MagicMock()
        response_data = controllers.compile(request_data, token, mock_session)
        data, code, headers = response_data
        self.assertEqual(code, status.SEE_OTHER)
        self.assertIn('Location', headers)
        self.assertIn(str(request_data['source_id']), headers['Location'])
        self.assertIn(request_data['checksum'], headers['Location'])
        self.assertIn(request_data['output_format'], headers['Location'])


class TestGetTask(TestCase):
    """Tests for :func:`controllers.get_status`."""

    def test_bad_checksum(self):
        """Request for status with a bad checksum value."""
        with self.assertRaises(BadRequest):
            controllers.get_status('1234', 'as12345!@#$', 'pdf')

    def test_bad_source_id(self):
        """Request for status with a bad source_id value."""
        with self.assertRaises(BadRequest):
            controllers.get_status('1234!@#$', 'as12345=', 'pdf')

    def test_bad_format(self):
        """Request for status with a bad output_format value."""
        with self.assertRaises(BadRequest):
            controllers.get_status('1234', 'as12345=', 'fdp')

    @mock.patch(f'{controllers.__name__}.url_for', mock_url_for)
    @mock.patch(f'{controllers.__name__}.compiler')
    def test_get_info_completed(self, mock_compiler):
        """Request for a completed compilation."""
        task_id = '123::asdf12345zxcv::pdf'
        source_id = '1234'
        checksum = 'asdf12345zxcv'
        output_format = 'pdf'
        mock_compiler.get_task.return_value \
            = Task(source_id=source_id,
                   output_format=Format.PDF,
                   status=Status.COMPLETED,
                   task_id=task_id,
                   checksum=checksum)
        response_data = controllers.get_status(source_id, checksum,
                                               output_format)
        data, code, headers = response_data
        self.assertEqual(code, status.OK)

    @mock.patch(f'{controllers.__name__}.url_for', mock_url_for)
    @mock.patch(f'{controllers.__name__}.compiler')
    def test_get_info_in_progress(self, mock_compiler):
        """Request for a compilation in progress."""
        task_id = 'task1234'
        source_id = '1234'
        checksum = 'asdf12345zxcv'
        output_format = 'pdf'
        mock_compiler.get_task.return_value \
            = Task(source_id=source_id,
                   output_format=Format.PDF,
                   status=Status.IN_PROGRESS,
                   task_id=task_id,
                   checksum=checksum)
        response_data = controllers.get_status(source_id, checksum,
                                               output_format)
        data, code, headers = response_data
        self.assertEqual(code, status.OK)

    @mock.patch(f'{controllers.__name__}.url_for', mock_url_for)
    @mock.patch(f'{controllers.__name__}.compiler')
    def test_get_info_nonexistant(self, mock_compiler):
        """Request for a nonexistant compilation."""
        mock_compiler.NoSuchTask = compiler.NoSuchTask
        source_id = '1234'
        checksum = 'asdf12345zxcv'
        output_format = 'pdf'
        mock_compiler.get_task.side_effect = compiler.NoSuchTask

        with self.assertRaises(NotFound):
            controllers.get_status(source_id, checksum, output_format)

    @mock.patch(f'{controllers.__name__}.url_for', mock_url_for)
    @mock.patch(f'{controllers.__name__}.compiler')
    def test_get_status_completed(self, mock_compiler):
        """Request for a completed compilation."""
        task_id = 'task1234'
        source_id = '1234'
        checksum = 'asdf12345zxcv'
        output_format = 'pdf'
        mock_compiler.get_task.return_value \
            = Task(source_id=source_id,
                   output_format=Format.PDF,
                   status=Status.COMPLETED,
                   task_id=task_id,
                   checksum=checksum)
        response_data = controllers.get_status(source_id, checksum,
                                               output_format)
        data, code, headers = response_data
        self.assertEqual(code, status.OK)

    @mock.patch(f'{controllers.__name__}.url_for', mock_url_for)
    @mock.patch(f'{controllers.__name__}.compiler')
    def test_get_status_in_progress(self, mock_compiler):
        """Request for a completed compilation."""
        task_id = 'task1234'
        source_id = '1234'
        checksum = 'asdf12345zxcv'
        output_format = Format.PDF
        mock_compiler.get_task.return_value \
            = Task(source_id=source_id,
                   output_format=Format.PDF,
                   status=Status.IN_PROGRESS,
                   task_id=task_id,
                   checksum=checksum)
        response_data = controllers.get_status(source_id, checksum,
                                               output_format.value)
        data, code, headers = response_data
        self.assertEqual(code, status.OK)


class TestGetProduct(TestCase):
    """Tests for :func:`controllers.get_product`."""

    def test_bad_checksum(self):
        """Request with a bad checksum value."""
        with self.assertRaises(BadRequest):
            controllers.get_product('1234', 'as12345!@#$', 'pdf')

    def test_bad_source_id(self):
        """Request with a bad source_id value."""
        with self.assertRaises(BadRequest):
            controllers.get_product('1234!@#$', 'as12345=', 'pdf')

    def test_bad_format(self):
        """Request with a bad output_format value."""
        with self.assertRaises(BadRequest):
            controllers.get_product('1234', 'as12345=', 'fdp')

    @mock.patch(f'{controllers.__name__}.url_for', mock_url_for)
    @mock.patch(f'{controllers.__name__}.compiler', mock.MagicMock())
    @mock.patch(f'{controllers.__name__}.Store')
    def test_get_product_completed(self, mock_store):
        """Request for a completed compilation product."""
        task_id = 'task1234'
        source_id = '1234'
        checksum = 'asdf12345zxcv'
        output_format = 'pdf'
        product_checksum = 'thechecksumoftheproduct'
        mock_store.current_session.return_value.retrieve.return_value \
            = Product(stream=io.BytesIO(b'foocontent'),
                      checksum=product_checksum)
        response_data = controllers.get_product(
            source_id,
            checksum,
            output_format
        )
        data, code, headers = response_data
        self.assertEqual(code, status.OK)
        self.assertEqual(headers['ETag'], product_checksum)

    @mock.patch(f'{controllers.__name__}.url_for', mock_url_for)
    @mock.patch(f'{controllers.__name__}.compiler')
    @mock.patch(f'{controllers.__name__}.Store')
    def test_get_product_nonexistant(self, mock_store, mock_compiler):
        """Request for a nonexistant compilation product."""
        mock_compiler.NoSuchTask = compiler.NoSuchTask
        source_id = '1234'
        checksum = 'asdf12345zxcv'
        output_format = 'pdf'
        mock_compiler.get_task.side_effect = compiler.NoSuchTask

        with self.assertRaises(NotFound):
            controllers.get_product(source_id, checksum, output_format)


class TestGetCompilationLog(TestCase):
    """Tests for :func:`controllers.get_log`."""

    def test_bad_checksum(self):
        """Request with a bad checksum value."""
        with self.assertRaises(BadRequest):
            controllers.get_log('1234', 'as12345!@#$', 'pdf')

    def test_bad_source_id(self):
        """Request with a bad source_id value."""
        with self.assertRaises(BadRequest):
            controllers.get_log('1234!@#$', 'as12345=', 'pdf')

    def test_bad_format(self):
        """Request with a bad output_format value."""
        with self.assertRaises(BadRequest):
            controllers.get_log('1234', 'as12345=', 'fdp')

    @mock.patch(f'{controllers.__name__}.url_for', mock_url_for)
    @mock.patch(f'{controllers.__name__}.compiler', mock.MagicMock())
    @mock.patch(f'{controllers.__name__}.Store')
    def test_get_log_completed(self, mock_store):
        """Request log for a completed compilation."""
        task_id = 'task1234'
        source_id = '1234'
        checksum = 'asdf12345zxcv'
        output_format = 'pdf'
        product_checksum = 'thechecksumoftheproduct'
        mock_store.current_session.return_value.retrieve_log.return_value \
            = Product(stream=io.BytesIO(b'foolog'),
                      checksum=product_checksum)
        response_data = controllers.get_log(
            source_id,
            checksum,
            output_format
        )
        data, code, headers = response_data
        self.assertEqual(code, status.OK)
        self.assertEqual(headers['ETag'], product_checksum)

    @mock.patch(f'{controllers.__name__}.url_for', mock_url_for)
    @mock.patch(f'{controllers.__name__}.compiler')
    @mock.patch(f'{controllers.__name__}.Store')
    def test_get_log_nonexistant(self, mock_store, mock_compiler):
        """Request for a nonexistant compilation log."""
        mock_compiler.NoSuchTask = compiler.NoSuchTask
        source_id = '1234'
        checksum = 'asdf12345zxcv'
        output_format = 'pdf'
        mock_compiler.get_task.side_effect = compiler.NoSuchTask

        with self.assertRaises(NotFound):
            controllers.get_log(source_id, checksum, output_format)
