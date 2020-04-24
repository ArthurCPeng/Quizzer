import pygame
import time
import random

pygame.init()
screen_width = 1100
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Quizzer")


#Questions and Answers
boxes = ["Class Ia","Class Ib","Class Ic","Class II","Class III","Class IV",
         "Cardiac Glycosides","Muscarinic Antagonists","Others"]
items = ["lidocaine","mexiletine","flecainide","encainide","propafenone",
         "procainamide","quinidine","disopyramide","propanolol",
         "metoprolol","esmolol","dofetilide","ibutilide","amiodarone",
         "dronedarone","sotalol","verapamil","diltiazem",
         "digoxin","atropine","adenosine"]

answer = {}
answer.setdefault(items[0],boxes[0])
answer.setdefault(items[1],boxes[0])

answer.setdefault(items[2],boxes[1])
answer.setdefault(items[3],boxes[1])
answer.setdefault(items[4],boxes[1])

answer.setdefault(items[5],boxes[2])
answer.setdefault(items[6],boxes[2])
answer.setdefault(items[7],boxes[2])

answer.setdefault(items[8],boxes[3])
answer.setdefault(items[9],boxes[3])
answer.setdefault(items[10],boxes[3])

answer.setdefault(items[11],boxes[4])
answer.setdefault(items[12],boxes[4])
answer.setdefault(items[13],boxes[4])
answer.setdefault(items[14],boxes[4])
answer.setdefault(items[15],boxes[4])

answer.setdefault(items[16],boxes[5])
answer.setdefault(items[17],boxes[5])

answer.setdefault(items[18],boxes[6])

answer.setdefault(items[19],boxes[7])

answer.setdefault(items[20],boxes[8])

#Size and configuration
max_columns = 5
box_margin_x = 20
box_margin_y = 20
box_height = 150
box_width = (screen_width - box_margin_x*(max_columns+1))/max_columns

item_width = 100
item_height = 40

box_number = len(boxes)
final_columns = box_number % max_columns
max_rows = int(box_number/max_columns) + 1
total_height = max_rows * box_height + (max_rows+1) * box_margin_y


#Font sizes 
box_font_value = 25
item_font_value = 25

#Font colors
original_color = (0,0,0)
correct_color = (0,255,0)
wrong_color = (255,0,0)
win_color = (255,0,0)



#Load box image
box_image = pygame.image.load('box.png')
box_image.convert_alpha()
box_image = pygame.transform.smoothscale(box_image,(int(box_width),int(box_height)))
box_position = box_image.get_rect()

#Load item image
item_image = pygame.image.load('item.png')
item_image.convert_alpha()
item_image = pygame.transform.smoothscale(item_image,(int(item_width),int(item_height)))
item_position = item_image.get_rect()


#Load item_selected image
item_selected_image = pygame.image.load('item_selected.png')
item_selected_image.convert_alpha()
item_selected_image = pygame.transform.smoothscale(item_selected_image,(int(item_width),int(item_height)))
item_selected_position = item_selected_image.get_rect()



#Define box class
class Box():
    def __init__(self, text, box_image, text_position_x, text_position_y):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(None, box_font_value)
        self.text_image = self.font.render(self.text, True, (255,0,0))

        self.box_image = box_image 

        
        self.text_position = self.text_image.get_rect()
        self.text_position.center = text_position_x, text_position_y

        self.box_position = box_image.get_rect()
        self.box_position.center = self.text_position.center

        self.solved = 0
        self.selected = 0


#Define item class
class Item():
    def __init__(self, text, position, item_image):
        super().__init__()
        self.text = text
        
        self.font = pygame.font.Font(None, item_font_value)
        self.text_image = self.font.render(text, True, original_color)
        
        self.item_image = item_image 

        
        self.text_position = self.text_image.get_rect()
        self.text_position.center = position[0],position[1]

        self.item_image_position = item_image.get_rect()
        self.item_image_position.center = position[0],position[1]

        self.correct = -1
        self.selected = 0
        self.collided = 0

        self.collided_text = ""
        
    def moveto(self,position):
        self.text_position.center = position
        self.item_image_position.center = position

    def refresh_picture(self,new_item_image):
        self.item_image = new_item_image 
        
    def refresh_color(self):
        if self.selected == 0:
            if self.correct == -1:
                self.text_image = self.font.render(self.text, True, original_color)
            if self.correct == 0:
                self.text_image = self.font.render(self.text, True, wrong_color)           
            if self.correct == 1:
                self.text_image = self.font.render(self.text, True, correct_color)
        if self.selected == 1:
            self.text_image = self.font.render(self.text, True, original_color)
        


#Creating new boxes and adding them to the list
box_objects = []
for box in boxes:
    
    box_font = pygame.font.Font(None, 60)
    box_text = box_font.render(box, True, (255,0,0))
    box_text_position = box_text.get_rect()

    
    index = boxes.index(box)
    
    column = index % max_columns
    row = int(index/max_columns) + 1

    
    #get the box position
    box_position.top = (row-1) * box_height + row * box_margin_y
    
    if row < max_rows:
        box_position.left = (column) * box_width + column * box_margin_x
    if row == max_rows:
        pad = (screen_width - (final_columns * box_width + (final_columns+1) * box_margin_x)) / 2
        box_position.left = pad + (column) * box_width + column * box_margin_x
    

    new_box = Box(box,box_image,box_position.center[0],box_position.center[1])
    box_objects.append(new_box)

#Creating new items and adding them to the list
item_objects = []
for item in items:
    new_item = Item(item, [random.randint(item_width,screen_width-item_width),
                           random.randint(total_height,screen_height - item_height)], item_image)
    item_objects.append(new_item)
    


#Start timer
start_time = time.time()


#Begin game
while True:
    all_correct = 1

    for event in pygame.event.get():
        #Selection
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()

            for item_object in item_objects:
                item_index = item_objects.index(item_object)
                if item_object.item_image_position.collidepoint(mouse_position):
                    item_object.selected = 1
                    item_object.refresh_picture(item_selected_image)
                    item_objects[item_index] = item_object
                    break

        #Deselection
        if event.type == pygame.MOUSEBUTTONUP:
            for item_object in item_objects:
                item_index = item_objects.index(item_object)
                if item_object.selected == 1:
                    #item_object.moveto(mouse_position)
                    item_object.selected = 0
                    item_object.refresh_picture(item_image)
                    item_objects[item_index] = item_object

    #Move selected item objects
    for item_object in item_objects:
        item_index = item_objects.index(item_object)
        mouse_position = pygame.mouse.get_pos()
        if item_object.selected == 1:
            item_object.moveto(mouse_position)
            item_objects[item_index] = item_object


    #Check for collision and see if answer is correct
    for item_object in item_objects:
        item_index = item_objects.index(item_object)



        item_object.collided = 0

        
        
        for box_object in box_objects:
            if item_object.item_image_position.colliderect(box_object.box_position):

                item_object.collided += 1
                item_object.collided_text = box_object.text


        if item_object.collided == 1:   #Only consider answer if only collide with one box 
            if answer[item_object.text] == item_object.collided_text:
                item_object.correct = 1
            else:
                item_object.correct = 0
        else:
            item_object.correct = -1
                

        item_object.collided = 0

        if item_object.collided > 1:
            item_object.collided = 1    

        item_objects[item_index] = item_object


    #Refresh color
    for item_object in item_objects:
        item_object.refresh_color()


    #Blit boxes
    for box_object in box_objects:
        screen.blit(box_object.box_image, box_object.box_position)
        screen.blit(box_object.text_image, box_object.text_position)


    #Blit items
    for i in range(0,len(item_objects)):
        item_object = item_objects[len(item_objects)-i-1]
        screen.blit(item_object.item_image, item_object.item_image_position)
        screen.blit(item_object.text_image, item_object.text_position)

    
    #Check if all correct
    for item_object in item_objects:
        if item_object.correct != 1 or item_object.selected == 1:
            all_correct = 0

    if all_correct == 1:
        time_used = round(time.time() - start_time,2)

        win_font = pygame.font.Font(None, 60)
        win_text = win_font.render("Your Time: " + str(time_used)+ " seconds", True, win_color)
        win_position = win_text.get_rect()
        win_position.center = screen_width/2, screen_height/2

        screen.blit(win_text, win_position)

        pygame.display.flip()
        break


    pygame.display.flip()
    screen.fill((255,255,255))


    

