import pygame
import time
import random

pygame.init()
screen_width = 1100
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Quizzer")


all_boxes = []
all_items = []
all_answers = []
all_questions = []

#---------- All Questions and Answers ----------#

#Questions and Answers

boxes_1 = ["Class Ia","Class Ib","Class Ic","Class II","Class III","Class IV",
         "Cardiac Glycosides","Muscarinic Antagonists","Others"]
items_1 = ["lidocaine","mexiletine","flecainide","encainide","propafenone",
         "procainamide","quinidine","disopyramide","propanolol",
         "metoprolol","esmolol","dofetilide","ibutilide","amiodarone",
         "dronedarone","sotalol","verapamil","diltiazem",
         "digoxin","atropine","adenosine"]
answer_1 = {}
answer_1.setdefault(items_1[0],boxes_1[1])
answer_1.setdefault(items_1[1],boxes_1[1])
answer_1.setdefault(items_1[2],boxes_1[2])
answer_1.setdefault(items_1[3],boxes_1[2])
answer_1.setdefault(items_1[4],boxes_1[2])
answer_1.setdefault(items_1[5],boxes_1[0])
answer_1.setdefault(items_1[6],boxes_1[0])
answer_1.setdefault(items_1[7],boxes_1[0])
answer_1.setdefault(items_1[8],boxes_1[3])
answer_1.setdefault(items_1[9],boxes_1[3])
answer_1.setdefault(items_1[10],boxes_1[3])
answer_1.setdefault(items_1[11],boxes_1[4])
answer_1.setdefault(items_1[12],boxes_1[4])
answer_1.setdefault(items_1[13],boxes_1[4])
answer_1.setdefault(items_1[14],boxes_1[4])
answer_1.setdefault(items_1[15],boxes_1[4])
answer_1.setdefault(items_1[16],boxes_1[5])
answer_1.setdefault(items_1[17],boxes_1[5])
answer_1.setdefault(items_1[18],boxes_1[6])
answer_1.setdefault(items_1[19],boxes_1[7])
answer_1.setdefault(items_1[20],boxes_1[8])

all_boxes.append(boxes_1)
all_items.append(items_1)
all_answers.append(answer_1)
all_questions.append("CPR22 Classes of Antiarrhythmic Drugs")



boxes_2 = ["Dihydropyridines","Benzothiazepine","Phenylalkylamine"]
items_2 = ["nifedipine","amlodipine","diltiazem","verapamil"]
answer_2 = {}
answer_2.setdefault(items_2[0],boxes_2[0])
answer_2.setdefault(items_2[1],boxes_2[0])
answer_2.setdefault(items_2[2],boxes_2[1])
answer_2.setdefault(items_2[3],boxes_2[2])

all_boxes.append(boxes_2)
all_items.append(items_2)
all_answers.append(answer_2)
all_questions.append("CPR40 Classes of Calcium Channel Blockers")



boxes_3 = ["First Generation (Non-Selective)","Second Generation (Cardiac-Selective)",
         "Third Generation (Beta Blockers with Vasodilator Effects)","Beta Blockers with Sympathomimetic Activity"]
items_3 = ["propranolol","metoprolol","bisoprolol","labetalol","carvedilol",
         "nebivolol","pindolol","acebutalol"]
answer_3 = {}
answer_3.setdefault(items_3[0],boxes_3[0])
answer_3.setdefault(items_3[1],boxes_3[1])
answer_3.setdefault(items_3[2],boxes_3[1])
answer_3.setdefault(items_3[3],boxes_3[2])
answer_3.setdefault(items_3[4],boxes_3[2])
answer_3.setdefault(items_3[5],boxes_3[2])
answer_3.setdefault(items_3[6],boxes_3[3])
answer_3.setdefault(items_3[7],boxes_3[3])
all_boxes.append(boxes_3)
all_items.append(items_3)
all_answers.append(answer_3)
all_questions.append("CPR40 Classes of Beta Blockers")






#---------- Size and Configuration of Images and Icons ----------#
#Size and configuration of home page
question_banks = len(all_boxes)
every_page = 2
pages = int(question_banks/every_page) + 1
question_box_height = 30
question_box_width = 600
question_box_margin = 20
list_top_displacement = 100

#Size and configuration of game page
max_columns = 5
box_margin_x = 20
box_margin_y = 20
box_height = 150
box_width = (screen_width - box_margin_x*(max_columns+1))/max_columns

item_width = 100
item_height = 40


#Configuration of return button
return_width = 75
return_height = 75
return_right_margin = 30
return_bottom_margin = 30

#Configuration of retry button
retry_width = 75
retry_height = 75
retry_left_margin = 30
retry_bottom_margin = 30

#Configuration of next page button
nextpage_right_margin = 30
nextpage_bottom_margin = 30

#Configuration of previous page button
previouspage_right_margin = 30
previouspage_bottom_margin = 30

#---------- Font Configuration ----------#
#Font sizes of game page
box_font_value = 25
item_font_value = 25

#Font sizes of home page
question_box_font_value = 30

#Font colors
original_color = (0,0,0)
correct_color = (0,255,0)
wrong_color = (255,0,0)
win_color = (255,0,0)


#---------- Load Images ----------#
#Load question box image
question_box_image = pygame.image.load('question_box.png')
question_box_image.convert_alpha()
question_box_image = pygame.transform.smoothscale(question_box_image,(int(question_box_width),int(question_box_height)))
question_box_position = question_box_image.get_rect()

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

#Load background image
background_image = pygame.image.load('background.jpg')
background_image.convert_alpha()
background_image = pygame.transform.smoothscale(background_image,(screen_width,screen_height))
background_position = background_image.get_rect()
background_position.left = 0
background_position.top = 0

#Load return image
return_image = pygame.image.load('return.png')
return_image.convert_alpha()
return_image = pygame.transform.smoothscale(return_image,(return_width,return_height))
return_position = return_image.get_rect()
return_position.right = screen_width - return_right_margin
return_position.bottom = screen_height - return_bottom_margin

#Load retry image
retry_image = pygame.image.load('retry.png')
retry_image.convert_alpha()
retry_image = pygame.transform.smoothscale(retry_image,(retry_width,retry_height))
retry_position = retry_image.get_rect()
retry_position.left = retry_left_margin
retry_position.bottom = screen_height - retry_bottom_margin

#Load next page image
nextpage_image = pygame.image.load('nextpage.png')
nextpage_image.convert_alpha()
nextpage_image = pygame.transform.smoothscale(nextpage_image,(int(100),int(100)))
nextpage_position = nextpage_image.get_rect()
nextpage_position.right = screen_width - nextpage_right_margin
nextpage_position.bottom = screen_height - nextpage_bottom_margin

#Load previous page image
previouspage_image = pygame.image.load('previouspage.png')
previouspage_image.convert_alpha()
previouspage_image = pygame.transform.smoothscale(previouspage_image,(int(100),int(100)))
previouspage_position = previouspage_image.get_rect()
previouspage_position.left =  previouspage_right_margin
previouspage_position.bottom = screen_height - previouspage_bottom_margin


#---------- Define Classes ----------#

#Define question box class
class QuestionBox():
    def __init__(self, text, question_box_image, text_position_x, text_position_y, index):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(None, question_box_font_value)
        self.text_image = self.font.render(self.text, True, (255,0,0))

        self.question_box_image = question_box_image

        self.text_position = self.text_image.get_rect()
        self.text_position.center = text_position_x, text_position_y

        self.question_box_position = question_box_image.get_rect()
        self.question_box_position.center = self.text_position.center

        self.selected = 0
        self.index = index

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

#---------- Sort all the question sets and create objects ----------#
all_questions_homepage = []
for page in range(0, pages):
    for i in range(0, every_page):
        # print("this index is "+str(page * every_page + i))

        if i == 0 and page * every_page + i != len(all_questions) - 1:
            new_questions_list = []
            new_questions_list.append(all_questions[page * every_page + i])

        if i == every_page - 1 or page * every_page + i == len(all_questions) - 1:
            if i == 0:
                new_questions_list = []

            new_questions_list.append(all_questions[page * every_page + i])

            all_questions_homepage.append(new_questions_list)

            # print("appended list with "+str(len(new_questions_list))+" items")

            if page * every_page + i == len(all_questions) - 1:
                break

        elif i != 0:
            new_questions_list.append(all_questions[page * every_page + i])

all_question_objects_list = []
for question_list in all_questions_homepage:
    #print("this list has " + str(len(question_list)) + " items")
    new_question_object_list = []
    for question in question_list:
        number = len(question_list)
        index = question_list.index(question)
        true_index = all_questions_homepage.index(question_list) * every_page + index
        position_y = list_top_displacement + question_box_height * index + question_box_margin * index
        #print(str(true_index)+"trueindex")
        #print(str(index)+"index")

        new_question_object = QuestionBox(question, question_box_image, screen_width/2, position_y, true_index)

        new_question_object_list.append(new_question_object)
    all_question_objects_list.append(new_question_object_list)

#---------- Define functions for creating and resetting boxes/objects ----------#
def reset_all_boxes(all_boxes):
    all_box_objects = []
    for boxes in all_boxes:

        box_number = len(boxes)
        final_columns = box_number % max_columns
        max_rows = int(box_number/max_columns) + 1
        total_height = max_rows * box_height + (max_rows+1) * box_margin_y

        #print(max_rows)
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
                box_position.left = (column) * box_width + (column+1) * box_margin_x
            if row == max_rows:
                pad = (screen_width - (final_columns * box_width + (final_columns+1) * box_margin_x)) / 2
                box_position.left = pad + (column) * box_width + column * box_margin_x

            new_box = Box(box,box_image,box_position.center[0],box_position.center[1])
            box_objects.append(new_box)
        all_box_objects.append(box_objects)

    return all_box_objects

def reset_all_items(all_items):
    all_item_objects = []

    for items in all_items:

        boxes = all_boxes[all_items.index(items)]
        box_number = len(boxes)
        final_columns = box_number % max_columns
        max_rows = int(box_number/max_columns) + 1
        total_height = max_rows * box_height + (max_rows+1) * box_margin_y

        item_objects = []
        for item in items:

            new_item = Item(item, [random.randint(item_width + retry_width + retry_left_margin,
                                                  screen_width-item_width - item_height - return_width - return_right_margin),
                                   random.randint(total_height,screen_height)], item_image)
            item_objects.append(new_item)
        all_item_objects.append(item_objects)

    return all_item_objects

#Creating all objects (initialization)
all_box_objects = reset_all_boxes(all_boxes)
all_item_objects = reset_all_items(all_items)


#Start timer
start_time = time.time()

#Start at homepage
game_status = -1

#print(len(all_question_objects_list))

#Begin game
while True:
    if game_status <= -1:

        page_number_index = -game_status - 1
        question_object_list = all_question_objects_list[page_number_index]

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                if nextpage_position.collidepoint(mouse_position):
                    game_status -= 1
                if previouspage_position.collidepoint(mouse_position):
                    game_status += 1

                if game_status >= -1:
                    game_status = -1
                if game_status <= -pages:
                    game_status = -pages

                #Selection of a game
                for question_object in question_object_list:
                    if question_object.question_box_position.collidepoint(mouse_position):
                        game_status = question_object.index
                        won = 0

                        # Start timer
                        start_time = time.time()

        #Blit the background
        screen.blit(background_image, background_position)

        #Blit the questions
        for question_object in question_object_list:
            screen.blit(question_object.question_box_image, question_object.question_box_position)
            screen.blit(question_object.text_image, question_object.text_position)

        #Blit the icons
        screen.blit(nextpage_image, nextpage_position)
        screen.blit(previouspage_image, previouspage_position)

        pygame.display.flip()
        screen.fill((255,255,255))


    if game_status > -1:
        
        item_objects = all_item_objects[game_status]
        box_objects = all_box_objects[game_status]
        answer = all_answers[game_status]

        all_correct = 1

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                
                #Setup to return to homepage
                if return_position.collidepoint(mouse_position):
                    game_status = -1
                    all_box_objects = reset_all_boxes(all_boxes)
                    all_item_objects = reset_all_items(all_items)
                    #continue

                #Setup to retry
                if retry_position.collidepoint(mouse_position):
                    won = 0
                    start_time = time.time()    
                    all_box_objects = reset_all_boxes(all_boxes)
                    all_item_objects = reset_all_items(all_items)
                    all_correct = 0
                    continue

            
            #Selection
            if event.type == pygame.MOUSEBUTTONDOWN and won == 0:
                mouse_position = pygame.mouse.get_pos()

                for item_object in item_objects:
                    item_index = item_objects.index(item_object)
                    if item_object.item_image_position.collidepoint(mouse_position):
                        item_object.selected = 1
                        item_object.refresh_picture(item_selected_image)
                        item_objects[item_index] = item_object
                        break


            #Deselection
            if event.type == pygame.MOUSEBUTTONUP and won == 0:
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

        #Blit return button
        screen.blit(return_image, return_position)

        #Blit retry button
        screen.blit(retry_image, retry_position)

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
            if won == 0:
                time_used = round(time.time() - start_time,2)

            win_font = pygame.font.Font(None, 60)
            win_text = win_font.render("Your Time: " + str(time_used)+ " seconds", True, win_color)
            win_position = win_text.get_rect()
            win_position.center = screen_width/2, screen_height/2

            screen.blit(win_text, win_position)

            pygame.display.flip()

            won = 1


        pygame.display.flip()
        screen.fill((255,255,255))




