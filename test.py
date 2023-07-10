import freeGPT 
import asyncio


# async def generate_text(prompt):
#     try:
#         resp = await getattr(freeGPT, "gpt3").Completion.create(prompt)
#         return resp
#     except Exception as e:
#         print(f"🤖: {e}")


# asyncio.run(generate_text())




import requests
r = requests.post('https://clipdrop-api.co/text-to-image/v1',
files = {
    'prompt': (None, 'photograph of a cat surfing', 'text/plain')
},
headers = { 'x-api-key': '9a605f7499c7f2b9a31d66744f89a6fcd2ca6ed5120589ae3ef726615c181b7cdc7c559584acd24d0d93485c221f785e'}
)
if (r.ok):
    with open('cat_surfing.jpg', 'wb') as f:
        # Write the content of the response to the file
        f.write(r.content)
# r.content contains the bytes of the returned image
else:
    r.raise_for_status()

# # {'id': '63d865fd-647d-4ea1-aa9d-8817753a44fc', 'output_url': 'https://api.deepai.org/job-view-file/63d865fd-647d-4ea1-aa9d-8817753a44fc/outputs/output.jpg'}
# print(r.json())



# import PyPDF2
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter

# # Retrieve the image and text from the 'boards' object
# # boards = Boards.objects.filter(board_id=user_board)
# # images = [board.image for board in boards]


# images = [r"C:\Users\abhis\Desktop\StoryBoard\krock\static\img\temp.jpg", r"C:\Users\abhis\Desktop\StoryBoard\krock\static\img\temp.jpg"]

# texts = ['helloodd', 'diuduiud d']

# from PIL import Image
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import cm

# from PIL import Image
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import cm

# def create_pdf(image_list, text_list, output_filename):
#     c = canvas.Canvas(output_filename, pagesize=A4)
#     width, height = A4

#     for i in range(len(image_list)):
        # img = Image.open(image_list[i])
        # img_width, img_height = img.size
        # aspect = img_height / float(img_width)

        # new_width = width
        # new_height = aspect * new_width

        # img = img.resize((int(new_width), int(new_height)))

        # img.save("temp.jpg")

        # c.drawImage("temp.jpg", width/2 - new_width/2, height/2 - new_height/2, width=new_width, height=new_height)
        # c.setFont("Helvetica", 14)
        # c.drawCentredString(width/2, height/2 - new_height/2 - 2*cm, text_list[i])  # Adjusted y-coordinate for text

        
        # c.line(0, 1*cm + 25, width, 1*cm + 25)  # Draw horizontal line
#         c.setFont("Helvetica", 12)
#         c.drawCentredString(width/2, 1*cm, "Title of the Document")
#         c.setFont("Helvetica", 10)
#         c.drawRightString(width - 1*cm, 1*cm, "Page {}/{}".format(i+1, len(image_list)))
#         c.showPage()

#     c.save()

# # Example usage:
# # image_list = ["image1.jpg", "image2.jpg", "image3.jpg"]
# # text_list = ["Text 1", "Text 2", "Text 3"]
# # create_pdf(image_list, text_list, "output.pdf")


# # Example usage:

# create_pdf(images, texts, "output.pdf")
