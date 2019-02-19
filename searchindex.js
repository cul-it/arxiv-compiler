Search.setIndex({docnames:["api/compiler","api/compiler.celery","api/compiler.celeryconfig","api/compiler.compiler","api/compiler.config","api/compiler.domain","api/compiler.factory","api/compiler.routes","api/compiler.services","api/compiler.services.filemanager","api/compiler.services.store","api/compiler.util","api/compiler.worker","api/modules","index"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.intersphinx":1,"sphinx.ext.viewcode":1,sphinx:55},filenames:["api/compiler.rst","api/compiler.celery.rst","api/compiler.celeryconfig.rst","api/compiler.compiler.rst","api/compiler.config.rst","api/compiler.domain.rst","api/compiler.factory.rst","api/compiler.routes.rst","api/compiler.services.rst","api/compiler.services.filemanager.rst","api/compiler.services.store.rst","api/compiler.util.rst","api/compiler.worker.rst","api/modules.rst","index.rst"],objects:{"":{compiler:[0,0,0,"-"]},"compiler.compiler":{CorruptedSource:[3,1,1,""],NoSuchTask:[3,1,1,""],TaskCreationFailed:[3,1,1,""],get_task:[3,2,1,""],run_docker:[3,2,1,""],start_compilation:[3,2,1,""],update_sent_state:[3,2,1,""]},"compiler.config":{APPLICATION_ROOT:[4,3,1,""],CONTAINER_SOURCE_ROOT:[4,3,1,""],DEBUG:[4,3,1,""],HOST_SOURCE_ROOT:[4,3,1,""],SERVER_NAME:[4,3,1,""],VERBOSE_COMPILE:[4,3,1,""]},"compiler.domain":{Format:[5,4,1,""],Product:[5,4,1,""],Reason:[5,4,1,""],SourcePackage:[5,4,1,""],SourcePackageInfo:[5,4,1,""],Status:[5,4,1,""],Task:[5,4,1,""]},"compiler.domain.Format":{DVI:[5,5,1,""],PDF:[5,5,1,""],PS:[5,5,1,""],content_type:[5,5,1,""],ext:[5,5,1,""]},"compiler.domain.Product":{checksum:[5,5,1,""],stream:[5,5,1,""],task:[5,5,1,""]},"compiler.domain.Reason":{AUTHORIZATION:[5,5,1,""],CANCELLED:[5,5,1,""],CORRUPTED:[5,5,1,""],ERROR:[5,5,1,""],MISSING:[5,5,1,""],NETWORK:[5,5,1,""],NONE:[5,5,1,""],SOURCE_TYPE:[5,5,1,""],STORAGE:[5,5,1,""]},"compiler.domain.SourcePackage":{etag:[5,5,1,""],path:[5,5,1,""],source_id:[5,5,1,""]},"compiler.domain.SourcePackageInfo":{etag:[5,5,1,""],source_id:[5,5,1,""]},"compiler.domain.Status":{COMPLETED:[5,5,1,""],FAILED:[5,5,1,""],IN_PROGRESS:[5,5,1,""]},"compiler.domain.Task":{Formats:[5,5,1,""],Statuses:[5,5,1,""],checksum:[5,5,1,""],content_type:[5,5,1,""],description:[5,5,1,""],ext:[5,5,1,""],from_dict:[5,6,1,""],output_format:[5,5,1,""],reason:[5,5,1,""],size_bytes:[5,5,1,""],source_id:[5,5,1,""],status:[5,5,1,""],task_id:[5,5,1,""],to_dict:[5,7,1,""]},"compiler.factory":{create_app:[6,2,1,""],jsonify_exception:[6,2,1,""]},"compiler.routes":{compile:[7,2,1,""],get_log:[7,2,1,""],get_product:[7,2,1,""],get_service_status:[7,2,1,""],get_status:[7,2,1,""]},"compiler.services":{filemanager:[9,0,0,"-"],store:[10,0,0,"-"]},"compiler.services.filemanager":{BadRequest:[9,1,1,""],BadResponse:[9,1,1,""],ConnectionFailed:[9,1,1,""],FileManagementService:[9,4,1,""],NotFound:[9,1,1,""],Oversize:[9,1,1,""],RequestFailed:[9,1,1,""],RequestForbidden:[9,1,1,""],RequestUnauthorized:[9,1,1,""],SecurityException:[9,1,1,""],current_session:[9,2,1,""],get_service_status:[9,2,1,""],get_session:[9,2,1,""],get_source_content:[9,2,1,""],get_upload_info:[9,2,1,""],init_app:[9,2,1,""],set_auth_token:[9,2,1,""]},"compiler.services.filemanager.FileManagementService":{get_service_status:[9,7,1,""],get_source_content:[9,7,1,""],get_upload_info:[9,7,1,""],request:[9,7,1,""],set_auth_token:[9,7,1,""]},"compiler.services.store":{DoesNotExist:[10,1,1,""],StoreSession:[10,4,1,""],create_bucket:[10,2,1,""],current_session:[10,2,1,""],get_session:[10,2,1,""],get_status:[10,2,1,""],hash_content:[10,2,1,""],init_app:[10,2,1,""],retrieve:[10,2,1,""],retrieve_log:[10,2,1,""],set_status:[10,2,1,""],store:[10,2,1,""],store_log:[10,2,1,""]},"compiler.services.store.StoreSession":{KEY:[10,5,1,""],LOG_KEY:[10,5,1,""],STATUS_KEY:[10,5,1,""],create_bucket:[10,7,1,""],get_status:[10,7,1,""],retrieve:[10,7,1,""],retrieve_log:[10,7,1,""],set_status:[10,7,1,""],store:[10,7,1,""],store_log:[10,7,1,""]},"compiler.util":{ResponseStream:[11,4,1,""]},compiler:{celery:[1,0,0,"-"],celeryconfig:[2,0,0,"-"],compiler:[3,0,0,"-"],config:[4,0,0,"-"],domain:[5,0,0,"-"],factory:[6,0,0,"-"],routes:[7,0,0,"-"],services:[8,0,0,"-"],util:[11,0,0,"-"],worker:[12,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","exception","Python exception"],"2":["py","function","Python function"],"3":["py","data","Python data"],"4":["py","class","Python class"],"5":["py","attribute","Python attribute"],"6":["py","classmethod","Python class method"],"7":["py","method","Python method"]},objtypes:{"0":"py:module","1":"py:exception","2":"py:function","3":"py:data","4":"py:class","5":"py:attribute","6":"py:classmethod","7":"py:method"},terms:{"boolean":3,"byte":[9,10,11],"class":[5,9,10,11],"default":[3,4,9,10],"enum":[5,10],"final":9,"function":3,"int":[3,7,9],"long":9,"new":[3,9,10],"return":[5,9],"true":[3,4,9],For:10,One:[5,10],The:[3,5,9,10],Used:10,Uses:10,abil:9,abl:9,about:[5,7,10],accept:9,action:10,add:3,addition:3,agnost:10,alia:5,allow:9,also:4,alwai:3,ani:[3,9,10],api:[9,10],app:[6,9,10],applic:[1,4,6,9,10,12],application_root:4,archiv:3,arg:3,argument:3,around:9,arxiv:10,associ:9,auth_error:5,authent:9,authn:9,author:5,auto_gen_p:3,autotex:3,autotex_timeout:3,avail:10,aws_access_key_id:10,aws_secret_access_kei:10,b64:5,badrequest:9,badrespons:9,base64:10,base:[3,5,9,10,11],befor:[3,10],being:[3,9],bodi:[3,10],bool:[3,9,10],botocor:10,bucket:10,buffer:5,cach:3,call:10,can:[3,4,10],cancel:5,celeri:[0,2,12,13],celeryconfig:[0,13],check:10,checksum:[3,5,7,10],chk:10,classmethod:5,client:[9,10],cmd:3,code:[3,9],command:3,compilation_error:5,complet:5,config:[0,13],configur:[2,4,9,10],conjunct:10,connect:9,connectionfail:9,contain:[4,9],container_dir:3,container_source_root:4,content:[3,5,9,10,14],content_path:9,content_typ:5,context:[4,9],control:10,convert:[3,4],cooki:4,copi:3,core:9,correspond:5,corrupt:[3,5],corrupted_sourc:5,corruptedsourc:3,could:[3,9],creat:[3,6,9,10],create_app:6,create_bucket:10,current:[5,7,9,10],current_sess:[9,10],cut:10,daemon:3,data:[5,9],debug:4,decryt:3,delet:3,descript:5,desir:3,determin:10,dev:4,dict:[5,9],did:5,differenti:3,dir:3,directori:[3,4,9],disabl:4,doc:2,docker:3,dockerfil:3,doe:[4,9,10],doesnotexist:10,domain:[0,3,4,9,10,13],don:3,down:10,downpath:9,dvi:[3,5],dvip:3,els:5,email:3,enabl:4,encapsul:9,encod:[5,10],endpoint:9,endpoint_url:10,error:[5,6],etag:5,everi:10,except:[3,6,9,10],exist:[3,5,9,10],exit:3,expected_cod:9,explan:5,expos:3,ext:[5,10],extens:5,extra:10,extract:3,facil:10,factori:[0,13],fail:[5,9],failur:5,fals:[3,4,10],field:5,file:[3,5,9,10],filemanag:[0,8],filemanagementservic:9,filenam:5,finm:3,flag:3,flask:[6,7,10],forev:3,format:[3,5,10],from:[3,5,9,10],from_dict:5,gener:[3,4,5,10],get:[3,7,9,10],get_log:7,get_product:7,get_service_statu:[7,9],get_sess:[9,10],get_source_cont:9,get_statu:[7,10],get_task:3,get_upload_info:9,getuid:3,going:3,gzip:3,handl:9,hash:[5,10],hash_cont:10,header:[3,9],help:4,helper:11,here:4,host_dir:3,host_source_root:4,http:9,identifi:[3,5,9,10],imag:[3,4],improp:9,in_progress:5,index:14,inform:[5,7],init_app:[9,10],initi:[1,12],instanc:[5,6,9],integr:[8,9],intend:10,intens:10,invalid_source_typ:5,invers:3,iter:11,itself:5,json:[6,10],jsonify_except:6,just:10,kei:[9,10],kind:5,kwarg:3,landscap:3,larg:9,launch:3,ledger:3,legal:3,letter:3,like:5,list:[3,10],live:[4,9],localhost:4,log:[3,7,10],log_kei:10,made:3,mai:5,make:3,malform:9,manag:[5,9,10],mani:9,md5:[5,10],messag:3,method:9,mime:5,miss:5,missing_sourc:5,mode:4,modul:[0,8,13,14],mount:3,move:3,msg:9,mutablemap:9,myapp:4,name:[3,4],need:10,network:5,network_error:5,non:3,none:[3,4,5,9,10],nosuchtask:3,note:4,notfound:9,number:[4,5],numer:3,object:[5,9,10,11],occupi:4,one:9,onli:3,option:[3,10],oserror:9,otherwis:9,our:3,out_fmt:10,outcom:5,output:[3,5],output_format:[3,5,7],overrid:3,overs:9,packag:[3,4,5,7,9,10,13,14],page:14,paper:[3,10],papernum:3,paramet:[3,9,10],pass:3,path:[4,5,9],pattern:10,pdf:[3,5],perform:9,port:[3,4],postscript:3,pre:3,preferred_compil:3,print:3,prior:9,process:[3,9],produc:11,product:[5,7,10],provid:10,ps_cach:3,ps_gen_tmp:3,psmapfil:3,quiet:3,rais:[9,10],rather:3,raw:5,read:9,readabl:5,reason:[5,10],receiv:9,referenc:9,region_nam:10,render:6,report:10,repositori:3,repres:[5,10],represent:[5,10],request:[3,4,5,7,9,10],requestfail:9,requestforbidden:9,requestunauthor:9,requir:[3,4,9,10],resourc:[9,10],respons:[7,9],responsestream:11,retriev:[5,9,10],retrieve_log:10,rout:[0,13],run:[3,4],run_dock:3,runtimeerror:[3,10],sanit:9,save:9,save_to:9,search:14,securityexcept:9,see:[2,10],self:[9,10],send:3,sender:3,sensibl:3,sent:3,server:4,server_nam:4,servic:[0,3,4,5,6,7,8,11],session:[4,9,10],set:[3,4,9,10],set_auth_token:9,set_statu:10,should:[9,10],similarli:10,simpl:3,size:5,size_byt:5,some:5,someth:5,sourc:[3,4,5,6,7,9,10,11],source_id:[3,5,7,9,10],source_typ:5,sourcepackag:[5,9],sourcepackageinfo:[5,9],specif:[3,5,10],src_id:10,ssl:9,stamp:3,start_compil:3,state:[3,5,9],statu:[3,5,7,9,10],status:5,status_kei:10,stderr:3,stdout:3,storag:[5,10],store:[0,5,8],store_log:10,storesess:10,str:[3,7,9,10],stream:[5,10,11],subdomain:4,submiss:9,submodul:13,subpackag:13,subsequ:9,support:[3,4,5],tag:3,take:10,tarbal:5,target:5,task:[3,5,7,10],task_id:5,taskcreationfail:3,tell:3,temporari:[3,4],test:10,tex_admin:3,thei:[3,9,10],thi:[3,4,5,9,10],through:3,time:10,tmp:[4,9],to_dict:5,token:[3,9],too:9,tupl:[3,5,9,10],type:5,underli:10,unexpect:9,union:7,uniqu:[3,5,9,10],updat:10,update_sent_st:3,upload:[5,9],uri:9,url:4,usag:3,use:[3,9,10],used:[3,9],user:[3,9],userid:3,uses:3,using:10,usual:5,util:[0,13],valu:[3,4],verbos:[3,4],verbose_compil:4,verifi:10,verify_cert:9,version:[3,10],volum:3,want:10,when:9,where:[4,10],whether:3,which:[9,10],whole:4,why:5,wish:3,without:4,work:3,worker:[0,13],workspac:[5,9],would:10,wrapper:[7,9,11],yymm:3},titles:["compiler package","compiler.celery module","compiler.celeryconfig module","compiler.compiler module","compiler.config module","compiler.domain module","compiler.factory module","compiler.routes module","compiler package","compiler.services.filemanager module","compiler.services.store module","compiler.util module","compiler.worker module","compiler","Welcome to arXiv Compilation Service\u2019s documentation!"],titleterms:{arxiv:14,celeri:1,celeryconfig:2,compil:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],config:4,document:14,domain:5,factori:6,filemanag:9,indic:14,modul:[1,2,3,4,5,6,7,9,10,11,12],packag:[0,8],rout:7,servic:[9,10,14],store:10,submodul:0,subpackag:[0,8],tabl:14,util:11,welcom:14,worker:12}})