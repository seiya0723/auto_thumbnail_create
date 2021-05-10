from django.shortcuts import render,redirect

# Create your views here.
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Photo,Document
from .forms import PhotoForm,DocumentForm

from django.conf import settings

import magic

#ALLOWED_MIME    = [ "application/pdf" ]
ALLOWED_MIME    = [ "image/vnd.adobe.photoshop","application/postscript" ]

class PhotoView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):

        photos    = Photo.objects.all()
        form    = PhotoForm()

        context = { "photos":photos,
                    "form":form,
                    }

        return render(request,"upload/index.html",context)

    def post(self, request, *args, **kwargs):

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = PhotoForm(copied, request.FILES)
        
        if form.is_valid():
            print("バリデーションOK")
            form.save()

        return redirect("upload:index")

index       = PhotoView.as_view()

class DocumentView(View):

    def get(self, request, *args, **kwargs):

        documents   = Document.objects.all()
        form        = DocumentForm()
        context = { "documents":documents,
                    "form":form,
                    }

        return render(request,"upload/document.html",context)

    def post(self, request, *args, **kwargs):

        #fileが指定されていない場合、後述の直接参照でインデックスエラーを防ぐためアーリーリターン
        if "file" not in request.FILES:
            return redirect("upload:document")

        mime_type   = magic.from_buffer(request.FILES["file"].read(1024) , mime=True)
        print(mime_type)

        #mime属性の保存(後のバッチ処理に繋げる)
        copied          = request.POST.copy()
        copied["mime"]  = mime_type

        form        = DocumentForm(copied,request.FILES)

        if not form.is_valid():
            print("バリデーションNG")
            return redirect("upload:document")

        if mime_type not in ALLOWED_MIME:
            print("このファイルは許可されていません。")
            return redirect("upload:document")


        print("バリデーションOK")
        result  = form.save() #TIPS:←返り値がモデルクラスのオブジェクトになるので、id属性を参照すれば良い。
        print(result.id)
        
        #======ここから先、サムネイル作成処理==========

        #処理結果のIDを元に、サムネイルの保存を行い、thumbnailに保存したパスを指定する
        document        = Document.objects.filter(id=result.id).first()

        #upload_to、settings内にあるMEDIA_ROOTを読み取り、そこに画像ファイルを保存。
        from django.conf import settings
        path            = Document.file.field.upload_to
        thumbnail_path  = path + str(document.id) + ".png"
        full_path       = settings.MEDIA_ROOT + "/" + thumbnail_path 

        #フォトショップの場合
        if document.mime == "image/vnd.adobe.photoshop":
            from psd_tools import PSDImage
            image   = PSDImage.open(settings.MEDIA_ROOT + "/" + str(document.file))
            image.composite().save(full_path)

        #イラストレーターの場合
        elif document.mime == "application/postscript":
            from PIL import Image
            image   = Image.open(settings.MEDIA_ROOT + "/" + str(document.file))
            image.save(full_path)
        else:
            return redirect("upload:document")

        document.thumbnail   = thumbnail_path
        document.save()


        """
        #TODO:方法1:MIMEを元にフォトショップデータ、もしくはAIデータからサムネイル生成。保存してデータを書き換える？要:idの控え←どうやってUUIDを控えるか？
        #TODO:方法2:データをバイナリで読み込んでサムネイル生成、DBに保存するか(1回のDB保存で済むが、バイナリで読まないといけないのでかなり難しい？)
        documents   = Document.objects.filter(id=result.id).first()
        documents.thumbnail  = "file/thumbnail/no-img23.png"
        documents.save()

        print(documents.id)
        print(documents.document)
        print(documents.thumbnail)

        #CHECK:これでmodels.pyに指定したupload_toを確認できる。
        #https://stackoverflow.com/questions/11796383/django-set-the-upload-to-in-the-view
        print(documents.document.field.upload_to)
        print(Document.document.field.upload_to)


        print(settings.MEDIA_ROOT + "/" + str(documents.document))
        print(settings.MEDIA_ROOT + "/" + str(documents.thumbnail))

        #TODO:これで方法1が再現できる。

        """


        return redirect("upload:document")

document    = DocumentView.as_view()
