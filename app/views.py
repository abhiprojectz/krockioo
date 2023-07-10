from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.views.generic import FormView
from django.urls import reverse
import json 
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from .decorators import only_authenticated_user, redirect_authenticated_user
import freeGPT
import asyncio
from .models import (UserBoards, Boards)
import random 
import uuid
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import io    
import base64
import json
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
import os 
import requests



class CreateBoard(View):
    def post(self, request):
        try:
            payload = json.loads(request.body)
            board_name = payload['board_name']
        except:
            return JsonResponse({'error': 'Invalid payload'}, status=400)

        # user = UserBoards.objects.get(user=request.user) 
        user = request.user
        print(user.id)
        max_id = 10 ** 10 - 1  
        board_id = random.randint(0, max_id) 
        user_board = UserBoards(user=user, board_id=board_id, board_image='/static/img/temp.jpg', board_name=board_name)
        user_board.save()

        return JsonResponse({'board_id': board_id}, status=201)
    


class CreateBoardSlide(View):
    def post(self, request):
        try:
            payload = json.loads(request.body)
            board_id = payload['board_id']
            slide_image = payload['slide_image']
            prompt_content = payload['prompt_content']
        except:
            return JsonResponse({'error': 'Invalid payload'}, status=400)

        user_board = UserBoards.objects.filter(board_id=board_id, user=request.user).first()
        if not user_board:
            return JsonResponse({'error': 'Invalid board ID'}, status=400)

        if slide_image == 'blank':
            slide_image = 'blank.png'

        max_id = 10 ** 10 - 1  
        slide_id = random.randint(0, max_id) 
        board = Boards(board_id=user_board, slide_id=slide_id, slide_image=slide_image, prompt_content=prompt_content)
        board.save()

        return JsonResponse({'board_id': board.board_id.board_id, 'slide_id': board.slide_id, 'slide_image': board.slide_image, 'prompt_content': board.prompt_content}, status=201)
    

class UpdateBoardSlide(View):
    def put(self, request):
        try:
            payload = json.loads(request.body)
            board_id = payload['board_id']
            board = Boards.objects.get(board_id__board_id=board_id)
        except:
            return JsonResponse({'error': 'Invalid payload or board ID'}, status=400)

        if board.board_id.user != request.user:
            return JsonResponse({'error': 'Unauthorized access'}, status=403)

        if 'slide_id' in payload:
            board.slide_id = payload['slide_id']
        if 'slide_image' in payload:
            board.slide_image = payload['slide_image']
        if 'prompt_content' in payload:
            board.prompt_content = payload['prompt_content']
        board.save()

        return JsonResponse({'board_id': board.board_id.board_id, 'slide_id': board.slide_id, 'slide_image': board.slide_image, 'prompt_content': board.prompt_content}, status=200)
    

   

class UpdateBoard(View):
    def put(self, request):
        try:
            payload = json.loads(request.body)
            board_id = payload['board_id']
            user_board = UserBoards.objects.get(board_id=board_id)
        except:
            return JsonResponse({'error': 'Invalid payload or board ID'}, status=400)

        if user_board.user != request.user:
            return JsonResponse({'error': 'Unauthorized access'}, status=403)

        if 'board_name' in payload:
            user_board.board_name = payload['board_name']
        user_board.save()

        return JsonResponse({'board_id': user_board.board_id, 'board_name': user_board.board_name}, status=200)



class Dashboard(View):
    template = "dashboard.html"
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        print(f"The ID is: {id}")
        
        user_board = UserBoards.objects.filter(board_id=id, user=request.user).first()
        boards = Boards.objects.filter(board_id=user_board)
        
        context = {'boards': boards,
                    'board_id': id,
                    'user_name': request.user,
                    'board_name':user_board.board_name,
                    'user_balance': request.user.balance
                    }
        return render(self.request, self.template, context)
    

from django.core import serializers
from django.http import JsonResponse


class GetAllBoards(View):
    def post(self, request):
        data = json.loads(request.body)
        
        user_board = UserBoards.objects.filter(board_id=data['board_id'] , user=request.user).first()
        boards = Boards.objects.filter(board_id=user_board)

        data = serializers.serialize('json', boards)
        response = JsonResponse({'output': data}, safe=False)
        return response


class GetAllSlides(View):
    def post(self, request):
        data = json.loads(request.body)
        
        boards = Boards.objects.filter(board_id=data['slide_id'])

        data = serializers.serialize('json', boards)
        response = JsonResponse({'output': data}, safe=False)
        return response
    

class AppPanel(View):
    template = "main_panel.html"
    def get(self, request, *args, **kwargs):
        user_boards = UserBoards.objects.filter(user=request.user)
        context = {'user_boards': user_boards,
                    'user_name': request.user,
                    "board_count": user_boards.count()
                   }
        return render(self.request, self.template, context)



class DeleteAllSlides(View):
    def post(self, request):
        data = json.loads(request.body)

        user_board = UserBoards.objects.filter(board_id=data['board_id'] , user=request.user).first()
        boards = Boards.objects.filter(board_id=user_board)
        boards.delete()
        return JsonResponse({'result': True})


class DeleteAllBoards(View):
    def post(self, request):
        user_board = UserBoards.objects.filter(user=request.user)
        user_board.delete()
        return JsonResponse({'result': True})


class DeleteBoard(View):
    def post(self, request):
        data = json.loads(request.body)

        user_board = UserBoards.objects.filter(board_id=data['board_id'] , user=request.user).first()
        boards = Boards.objects.filter(board_id=user_board)
        user_board.delete()
        return JsonResponse({'result': True})


class DeleteSlide(View):
    def post(self, request):
        data = json.loads(request.body)
        board = Boards.objects.filter(slide_id=data['slide_id']).first()
        board.delete()
        return JsonResponse({'result': True})
    
class GenerateAllImages(View):
    def post(self, request):
        data = json.loads(request.body)
        image_style = data['image_style']
        print(data['board_id'])

        user_board = UserBoards.objects.filter(board_id=data['board_id'] , user=request.user).first()
        boards = Boards.objects.filter(board_id=user_board)


        for board in boards:
            response = requests.post('https://clipdrop-api.co/text-to-image/v1',
            files = {
                'prompt': (None, str(board.prompt_content + ' , in ' + image_style + ' style'), 'text/plain')
            },
            headers = { 'x-api-key': '9a605f7499c7f2b9a31d66744f89a6fcd2ca6ed5120589ae3ef726615c181b7cdc7c559584acd24d0d93485c221f785e'}
            )

            if response.status_code == 200:
                # Get the filename from the URL
                filename = str(uuid.uuid4())[:10]

                # Define the path to save the image in the static folder
                save_path = os.path.join(str(os.path.join(settings.BASE_DIR, 'static')) + '/img/', filename + '.png')
                url_path = '/static/img/' + filename +  '.png'
                # Save the image to the static folder
                with open(save_path, 'wb') as f:
                    f.write(response.content)

            board = Boards.objects.get(slide_id=board.slide_id)
            board.slide_image = url_path
            board.save()

        return JsonResponse({'result': True})



class DownloadPDF(View):
    def post(self, request):
        data = json.loads(request.body)

        user_board = UserBoards.objects.filter(board_id=data['board_id'] , user=request.user).first()
        boards = Boards.objects.filter(board_id=user_board)

        image_list = []
        text_list = []
        _title = user_board.board_name

        for i in boards:
            image_list.append(i.slide_image)
            text_list.append(i.prompt_content)

        # output_filename = "output.pdf"
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        for i in range(len(image_list)):
            _img = str(settings.BASE_DIR) + '/' + image_list[i]
            img = Image.open(_img)
            img_width, img_height = img.size
            aspect = img_height / float(img_width)

            new_width = width
            new_height = aspect * new_width

            img = img.resize((int(new_width), int(new_height)))

            img.save(_img)

            c.drawImage(_img, width/2 - new_width/2, height/2 - new_height/2, width=new_width, height=new_height)
            c.setFont("Helvetica", 14)
            c.drawCentredString(width/2, height/2 - new_height/2 - 2*cm, text_list[i])
            c.line(0, 1*cm + 25, width, 1*cm + 25)
            c.setFont("Helvetica", 12)
            c.drawCentredString(width/2, 1*cm, str(_title).capitalize())
            c.setFont("Helvetica", 10)
            c.drawRightString(width - 1*cm, 1*cm, "Page {}/{}".format(i+1, len(image_list)))
            c.showPage()


        c.save()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')



class UpdateText(View):
    def post(self, request):
        data = json.loads(request.body)

        slide_id = data['slide_id'] 
        prompt = data['text_prompt']

        board = Boards.objects.get(slide_id=slide_id)
        board.prompt_content = prompt
        board.save()
        return JsonResponse({'output': True})


class GenerateImage(View):
    def post(self, request):
        data = json.loads(request.body)

        slide_id = data['slide_id'] 
        board = Boards.objects.get(slide_id=slide_id)
        

        prompt = board.prompt_content 
        image_style = data['image_style']


        response = requests.post('https://clipdrop-api.co/text-to-image/v1',
        files = {
            'prompt': (None, prompt, 'text/plain')
        },
        headers = { 'x-api-key': '9a605f7499c7f2b9a31d66744f89a6fcd2ca6ed5120589ae3ef726615c181b7cdc7c559584acd24d0d93485c221f785e'}
        )

        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

        if response.status_code == 200:
            # Get the filename from the URL
            filename = str(uuid.uuid4())[:10]

            # Define the path to save the image in the static folder
            save_path = os.path.join(str(os.path.join(settings.BASE_DIR, 'static')) + '/img/', filename + '.png')
            url_path = '/static/img/' + filename +  '.png'
            # Save the image to the static folder
            with open(save_path, 'wb') as f:
                f.write(response.content)


        board.slide_image = url_path
        board.save()

        return JsonResponse({'output': True})

# Using openai
# async def generate_text(prompt):
#     url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {os.environ.get("OPENAI_API")}'
#     }

#     # Define the prompt and parameters for the API request
#     data = {
#         'prompt': prompt,
#         'max_tokens': 64,
#         'temperature': 0.7
#     }

#     # Send the API request and get the response
#     response = requests.post(url, headers=headers, json=data)

#     # Extract the generated text from the response
#     text = response.json()['choices'][0]['text'].strip()
#     return text

async def generate_text(prompt):
    try:
        resp = await getattr(freeGPT, "gpt3").Completion.create(prompt)
        return resp
    except Exception as e:
        print(f"🤖: {e}")




class GenerateSuggestion(View):
    def post(self, request):
        data = json.loads(request.body)
        prompt = 'Your task is to write a storyline suggestion script in 2-3 sentences. Output only in required format. Do not write or explain/replies anything.'


        response = asyncio.run(generate_text(prompt))
        print(response)

        res = {'output': response}

        return JsonResponse({'output': res})





class GenerateTextView(View):
    def post(self, request):
        data = json.loads(request.body)
        prompt = 'Your task is to write a storylines in below given sentences count based on the short description given below. Output only in required format. Do not write or explain/replies anything. Short description: '
        prompt += data['text_prompt'] + ' '
        if data['count_frames'] == '5-10':
            prompt += 'You need to write between 5 to 10 sentences.'
        elif data['count_frames'] == '10-15':
            prompt += 'You need to write between 10 to 15 sentences.'
        elif data['count_frames'] == '15-20':
            prompt += 'You need to write between 15 to 20 sentences.'

        prompt += 'Output only the storylines sentences in a form of a string list containing all sentences.Strictly follow this format.'

        response = asyncio.run(generate_text(prompt))
        print(response)

        res = {'output': response}

        user_board = UserBoards.objects.filter(board_id=data['board_id'], user=request.user).first()
        if not user_board:
            return JsonResponse({'error': 'Invalid board ID'}, status=400)

        slide_image = 'blank.png'

        result = []

        for i in json.loads(res['output']):
            max_id = 10 ** 10 - 1  
            slide_id = random.randint(0, max_id) 
            board = Boards(board_id=user_board, slide_id=slide_id, slide_image=slide_image, prompt_content=i)
            board.save()
            board = {
                "board_id": data['board_id'],
                "slide_id": slide_id,
                "slide_image": slide_image,
                "prompt_content": i
            }
            result.append(board)

        return JsonResponse({'output': result})


