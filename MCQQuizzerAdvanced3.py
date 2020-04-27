import pygame
import time
import random
import os

pygame.init()
screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MCQ Quizzer")

all_question_sets = []
all_question_set_names = []
all_answer_sets = []
submitted = []
start_times = []
times = []
correct_counts = []
wrong_counts = []
scores = []
started = []


#------------------------------Configuration of Images and Icons------------------------------#


#------Configuration of General Elements------#

#--next page button--#
nextpage_right_margin = 30
nextpage_bottom_margin = 30

#--previous page button--#
previouspage_right_margin = 30
previouspage_bottom_margin = 30

#--return button--#
return_width = 75
return_height = 75
return_left_margin = 30
return_top_margin = 30

#------Configuration of Homepage Elements------#

#--Homepage Question Box--#
homepage_question_box_width = 600
homepage_question_box_height = 30
homepage_question_box_margin = 15
homepage_question_font_value = 25
list_top_displacement = 150

#------Configuration of Testing Page Elements------#

pad = 10
line_margin = 5

#--Question Box--#

question_box_height = 200
question_box_width = 600
question_font_value = 30
top_displacement = 120

max_question_line_length = 100
question_color = (0,0,255)

#--Choice Box--#
choice_box_width = 600
choice_box_height = 30
choice_font_value = 25

first_margin = 50
choice_margin = 10

max_choice_line_length = 150
choice_color = (0,0,0)

#--Star--#
star_height = 50
star_width = 50
star_top_margin = 40

#--Unattempted Sign--#
unattempted_height = 60
unattempted_width = 203
unattempted_bottom_margin = 30

#--Mainpage icon--#
mainpage_width = 75
mainpage_height = 75
mainpage_icon_font_value = 25
mainpage_icon_color = (0,0,0)
mainpage_right_margin = 30
mainpage_top_margin = 30

#------Configuration of Mainpage Elements------#

#---question icons---#
question_icon_width = 40
question_icon_height = 58

question_icon_columns = 5
question_icon_rows = 3
question_icon_padx = 200
question_icon_top_displacement = 150
question_icon_bottom_displacement = 80
question_icon_marginx = (screen_width - question_icon_padx * 2 - question_icon_width * question_icon_columns) / (question_icon_columns - 1)
question_icon_marginy = (screen_height - question_icon_top_displacement - question_icon_bottom_displacement - question_icon_height * question_icon_rows) / (question_icon_rows - 1)
question_icon_marginy = 20


#--Submit button--#
submit_bottom_margin = 30
submit_width = 75
submit_height = 75

#--Result display--#
result_first_displacement = 60
result_second_displacement = 90
result_font_value = 30
result_color = (255,0,0)


#------------------------------Define Classes------------------------------#

class QuestionIcon():
    def __init__(self, question, index, position_x, position_y):
        self.question = question
        self.index = index
        
        if self.question.chosen == 0 and self.question.starred == -1:
            self.question_icon_image =  question_icon_image
        if self.question.chosen == 1 and self.question.starred == -1:
            self.question_icon_image = question_icon_chosen_image
        if self.question.chosen == 0 and self.question.starred == 1:
            self.question_icon_image = question_icon_starred_image
        if self.question.chosen == 1 and self.question.starred == 1:
            self.question_icon_image = question_icon_chosen_starred_image

        self.question_icon_position = self.question_icon_image.get_rect()
        self.question_icon_position.center = position_x, position_y

        self.font = pygame.font.Font(None, mainpage_icon_font_value)
        self.number = self.font.render(str(index+1), True, mainpage_icon_color)
        
        self.number_position = self.number.get_rect()
        self.number_position.center = position_x, position_y - question_icon_height/4


    def blit_questionicon(self):
        screen.blit(self.question_icon_image, self.question_icon_position)
        screen.blit(self.number, self.number_position)

    def blit_submitted_icon(self):
        if self.question.correct == 1:
            screen.blit(question_icon_correct_image, self.question_icon_position)
            screen.blit(self.number, self.number_position)
        if self.question.correct == 0:
            screen.blit(question_icon_wrong_image, self.question_icon_position)
            screen.blit(self.number, self.number_position)
        if self.question.chosen == 0:
            screen.blit(question_icon_unselected_image, self.question_icon_position)
            screen.blit(self.number, self.number_position)         
            


class QuestionBox():
    def __init__(self, text, question_box_image, text_position_x, text_position_y, index):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(None, homepage_question_font_value)
        self.text_image = self.font.render(self.text, True, (255,0,0))

        self.question_box_image = question_box_image

        self.text_position = self.text_image.get_rect()
        self.text_position.center = text_position_x, text_position_y

        self.question_box_position = question_box_image.get_rect()
        self.question_box_position.center = self.text_position.center

        self.selected = 0
        self.index = index

class Choice():
    def __init__(self, text, correct, box_image, position_x, position_y, max_line_length, color, font_value):
        self.correct = correct

        
        self.text = text
        self.selected = -1
        
        self.box_image = box_image
        self.box_position = self.box_image.get_rect()
        self.box_position.center = position_x, position_y
        
        
        lines = []
        text_list = self.text.split(" ")
        new_line = ""
        for word in text_list:
            word_index = text_list.index(word)
    
            if len(new_line + word) > max_line_length:
                if word_index != 0:
                    lines.append(new_line)
                new_line = word + " "
                if word_index == len(text_list) - 1:
                    lines.append(new_line)
                
            else:
                new_line += word + " "
                if word_index == len(text_list) - 1:
                    lines.append(new_line)
                

            '''     
            if word_index % words_per_line == 0:
                new_line = ""
                new_line += word
                new_line += " "
                
                if  word_index == len(text_list) -1:
                    lines.append(new_line)
                    break   
            if (word_index % words_per_line == words_per_line - 1) or word_index == len(text_list) -1:
                new_line += word
                lines.append(new_line)
                new_line = ""
                if  word_index == len(text_list) -1:
                    break
    
            if word_index % words_per_line != 0 and word_index % words_per_line != words_per_line - 1 and word_index == len(text_list) -1:
                new_line += word
                new_line += " "
            '''

        self.text_images = []
        self.text_positions = []
        
        for line in lines:
            line_number = lines.index(line)
            
            font = pygame.font.Font(None, font_value)
            text_image = font.render(line, True, color)
            
            text_position = text_image.get_rect()
            text_height = text_position.bottom - text_position.top
            
            text_position.top = position_y - (len(lines)/2 - line_number) * text_height - (len(lines)/2 - line_number - 0.5) * line_margin
            text_position.left = self.box_position.left + pad 


            self.text_positions.append(text_position)
            self.text_images.append(text_image)


    def blit(self):
        screen.blit(self.box_image, self.box_position)
        
        for text_image in self.text_images:
            text_position = self.text_positions[self.text_images.index(text_image)]
            screen.blit(text_image, text_position)

    def refresh_picture(self, new_box_image):
        self.box_image = new_box_image
        


class Question():
    def __init__(self, question, answer, question_box_image, choice_box_image, question_font_value, choice_font_value):
        
        self.question = Choice(question, -2, question_box_image,screen_width/2,
                               top_displacement + question_box_height/2, max_question_line_length,
                               question_color, question_font_value)
        
        self.choices = []
        self.chosen = 0 

        self.choices_temp = []

        self.choice_box_image = choice_box_image
        self.correct = 0
        self.starred = -1

        self.answer = answer #get answer


    def get_choices(self, new_choice):
        self.choices_temp.append(new_choice)

    def create_choices(self):
        choice_number = len(self.choices_temp)
        for choice_text in self.choices_temp:

            index = self.choices_temp.index(choice_text)
            
            if len(self.choices) == int(self.answer) -1:
                correct = 1
            else:
                correct = 0

            position_y = top_displacement + question_box_height + choice_box_height * index + first_margin + choice_margin * index

            new_choice_object = Choice(choice_text, correct, self.choice_box_image,
                                       screen_width / 2, position_y,
                                       max_choice_line_length, choice_color, choice_font_value)
            
            self.choices.append(new_choice_object) 


    def blit_question(self):
        screen.blit(self.question.box_image, self.question.box_position)
        self.question.blit()
        for choice in self.choices:
            choice.blit()

#------------------------------Load Images------------------------------#

#Load homepage question box image
homepage_question_box_image = pygame.image.load('homepage_question_box.png')
homepage_question_box_image.convert_alpha()
homepage_question_box_image = pygame.transform.smoothscale(homepage_question_box_image,(int(homepage_question_box_width),int(homepage_question_box_height)))
homepage_question_box_position = homepage_question_box_image.get_rect()


#Load question box image
question_box_image = pygame.image.load('question_box.png')
question_box_image.convert_alpha()
question_box_image = pygame.transform.smoothscale(question_box_image,(int(question_box_width),int(question_box_height)))
question_box_position = question_box_image.get_rect()

#Load choice box image
choice_box_image = pygame.image.load('choice_box.png')
choice_box_image.convert_alpha()
choice_box_image = pygame.transform.smoothscale(choice_box_image,(int(choice_box_width),int(choice_box_height)))
choice_box_position = choice_box_image.get_rect()

#Load question icon image
question_icon_image = pygame.image.load('question_icon.png')
question_icon_image.convert_alpha()
question_icon_image = pygame.transform.smoothscale(question_icon_image,(int(question_icon_width),int(question_icon_height)))
question_icon_position = question_icon_image.get_rect()

#Load chosen question icon image
question_icon_chosen_image = pygame.image.load('question_icon_chosen.png')
question_icon_chosen_image.convert_alpha()
question_icon_chosen_image = pygame.transform.smoothscale(question_icon_chosen_image,(int(question_icon_width),int(question_icon_height)))
question_icon_chosen_position = question_icon_chosen_image.get_rect()

#Load starred question icon image
question_icon_starred_image = pygame.image.load('question_icon_starred.png')
question_icon_starred_image.convert_alpha()
question_icon_starred_image = pygame.transform.smoothscale(question_icon_starred_image,(int(question_icon_width),int(question_icon_height)))
question_icon_starred_position = question_icon_starred_image.get_rect()

#Load selected and starred question icon image
question_icon_chosen_starred_image = pygame.image.load('question_icon_chosen_starred.png')
question_icon_chosen_starred_image.convert_alpha()
question_icon_chosen_starred_image = pygame.transform.smoothscale(question_icon_chosen_starred_image,(int(question_icon_width),int(question_icon_height)))
question_icon_chosen_starred_position = question_icon_chosen_starred_image.get_rect()


#Load wrong question icon image
question_icon_wrong_image = pygame.image.load('question_icon_wrong.png')
question_icon_wrong_image.convert_alpha()
question_icon_wrong_image = pygame.transform.smoothscale(question_icon_wrong_image,(int(question_icon_width),int(question_icon_height)))
question_icon_wrong_position = question_icon_wrong_image.get_rect()

#Load correct question icon image
question_icon_correct_image = pygame.image.load('question_icon_correct.png')
question_icon_correct_image.convert_alpha()
question_icon_correct_image = pygame.transform.smoothscale(question_icon_correct_image,(int(question_icon_width),int(question_icon_height)))
question_icon_correct_position = question_icon_correct_image.get_rect()

#Load unselected question icon image
question_icon_unselected_image = pygame.image.load('question_icon_unselected.png')
question_icon_unselected_image.convert_alpha()
question_icon_unselected_image = pygame.transform.smoothscale(question_icon_unselected_image,(int(question_icon_width),int(question_icon_height)))
question_icon_unselected_position = question_icon_unselected_image.get_rect()



#Load selected choice box image
choice_box_selected_image = pygame.image.load('choice_box_selected.png')
choice_box_selected_image.convert_alpha()
choice_box_selected_image = pygame.transform.smoothscale(choice_box_selected_image,(int(choice_box_width),int(choice_box_height)))
choice_box_selected_position = choice_box_selected_image.get_rect()


#Load correct choice box image
choice_box_correct_image = pygame.image.load('choice_box_correct.png')
choice_box_correct_image.convert_alpha()
choice_box_correct_image = pygame.transform.smoothscale(choice_box_correct_image,(int(choice_box_width),int(choice_box_height)))
choice_box_correct_position = choice_box_correct_image.get_rect()

#Load correct but unselected choice box image
choice_box_correct_unselected_image = pygame.image.load('choice_box_correct_unselected.png')
choice_box_correct_unselected_image.convert_alpha()
choice_box_correct_unselected_image = pygame.transform.smoothscale(choice_box_correct_unselected_image,(int(choice_box_width),int(choice_box_height)))
choice_box_correct_unselected_position = choice_box_correct_unselected_image.get_rect()

#Load wrong choice box image
choice_box_wrong_image = pygame.image.load('choice_box_wrong.png')
choice_box_wrong_image.convert_alpha()
choice_box_wrong_image = pygame.transform.smoothscale(choice_box_wrong_image,(int(choice_box_width),int(choice_box_height)))
choice_box_wrong_position = choice_box_wrong_image.get_rect()

#Load background image
background_image = pygame.image.load('background.jpg')
background_image.convert_alpha()
background_image = pygame.transform.smoothscale(background_image,(screen_width,screen_height))
background_position = background_image.get_rect()
background_position.left = 0
background_position.top = 0

#load mainpage background
mainpage_background_image = pygame.image.load('mainpage_background.png')
mainpage_background_image.convert_alpha()
mainpage_background_image = pygame.transform.smoothscale(mainpage_background_image,(screen_width,screen_height))
mainpage_background_position = mainpage_background_image.get_rect()
mainpage_background_position.left = 0
mainpage_background_position.top = 0

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

#Load return image
return_image = pygame.image.load('return.png')
return_image.convert_alpha()
return_image = pygame.transform.smoothscale(return_image,(return_width,return_height))
return_position = return_image.get_rect()
return_position.left = return_left_margin
return_position.top = return_top_margin

#Load unattempted image
unattempted_image = pygame.image.load('unattempted.png')
unattempted_image.convert_alpha()
unattempted_image = pygame.transform.smoothscale(unattempted_image,(unattempted_width,unattempted_height))
unattempted_position = unattempted_image.get_rect()
unattempted_position.center = screen_width / 2, screen_height
unattempted_position.bottom = screen_height - unattempted_bottom_margin


#Load mainpage icon
mainpage_image = pygame.image.load('mainpage.png')
mainpage_image.convert_alpha()
mainpage_image = pygame.transform.smoothscale(mainpage_image,(mainpage_width, mainpage_height))
mainpage_position = mainpage_image.get_rect()
mainpage_position.right = screen_width - mainpage_right_margin
mainpage_position.top = mainpage_top_margin


#Load star image
star_image = pygame.image.load('star.png')
star_image.convert_alpha()
star_image = pygame.transform.smoothscale(star_image, (star_width, star_height))
star_position = star_image.get_rect()
star_position.center = screen_width/2, screen_height
star_position.top = star_top_margin

#Load selected star image
selected_star_image = pygame.image.load('selected_star.png')
selected_star_image.convert_alpha()
selected_star_image = pygame.transform.smoothscale(selected_star_image,(star_width, star_height))
selected_star_position = selected_star_image.get_rect()
selected_star_position.center = screen_width/2, screen_height
selected_star_position.top = star_top_margin


#Load submit image
submit_image = pygame.image.load('submit.png')
submit_image.convert_alpha()
submit_image = pygame.transform.smoothscale(submit_image, (submit_width, submit_height))
submit_position = submit_image.get_rect()
submit_position.center = screen_width/2, screen_height
submit_position.bottom = screen_height - submit_bottom_margin



#------------------------------Read Files------------------------------#
file_list = os.listdir("MCQ")
folder = "/Users/arthur/Documents/Python/Projects/Quizzer/MCQ/"

for file in file_list:
    if file == ".DS_Store":
        continue

    all_question_set_names.append(file[:len(file)-4])
    #print(file)
    #print("appended")
    #print(len(all_question_set_names))

    new_question_set = []

    document = open(folder+file, "r")
    text = document.read()
    questions = text.split("\n\n")


    for question in questions:
        lines = question.split("\n")
        question_text = lines[0]
        answer = lines[1]
        choices = lines[2:]
        question_object = Question(question_text, answer, question_box_image, choice_box_image,
                                   question_font_value, choice_font_value)
        
        for choice in choices:
            question_object.get_choices(choice)
            
        question_object.create_choices()

        new_question_set.append(question_object)

    all_question_sets.append(new_question_set)
    submitted.append(0)
    times.append(0)
    start_times.append(0)
    correct_counts.append(0)
    wrong_counts.append(0)
    scores.append(0)
    started.append(0)



question_sets = len(all_question_sets)
every_page = 5

if round(question_sets/every_page) != question_sets/every_page:
    pages = int(question_sets/every_page) + 1
else:
    pages = int(question_sets/every_page)


#------------------------------Create Homepage Objects------------------------------#

all_questions_homepage = []
for page in range(0, pages):
    for i in range(0, every_page):

        if i == 0 and page * every_page + i != len(all_question_set_names) - 1:
            new_questions_list = []
            new_questions_list.append(all_question_set_names[page * every_page + i])

        if i == every_page - 1 or page * every_page + i == len(all_question_set_names) - 1:
            if i == 0:
                new_questions_list = []

            new_questions_list.append(all_question_set_names[page * every_page + i])

            all_questions_homepage.append(new_questions_list)


            if page * every_page + i == len(all_question_set_names) - 1:
                break

        elif i != 0:
            new_questions_list.append(all_question_set_names[page * every_page + i])


all_question_objects_list = []
for question_list in all_questions_homepage:

    new_question_object_list = []
    
    for question in question_list:
        number = len(question_list)
        index = question_list.index(question)
        true_index = all_questions_homepage.index(question_list) * every_page + index
        position_y = list_top_displacement + homepage_question_box_height * index + homepage_question_box_margin * index

        new_question_object = QuestionBox(question, homepage_question_box_image, screen_width/2, position_y, true_index)

        new_question_object_list.append(new_question_object)
    all_question_objects_list.append(new_question_object_list)





#------------------------------Start Game------------------------------#

game_status = [0,0,0,0]

while True:

    #---------------Homepage---------------#

    
    if game_status[0] == 0:

        page_number_index = game_status[1]
        
        question_object_list = all_question_objects_list[page_number_index]

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                
                #--Flip page--#
                if nextpage_position.collidepoint(mouse_position):
                    game_status = [game_status[0],game_status[1]+1,0,0]
                if previouspage_position.collidepoint(mouse_position):
                    game_status = [game_status[0],game_status[1]-1,0,0]

                if game_status[1] < 0:
                    game_status = [game_status[0],0,0,0]  #Make sure page does not go out of range
                if game_status[1] >= pages:
                    game_status = [game_status[0],pages-1,0,0] #Make sure page does not go out of range

                #--Select a question set--#
                for question_object in question_object_list:
                    if question_object.question_box_position.collidepoint(mouse_position):
                        game_status = [1,question_object.index,0,0]

                        if started[question_object.index] == 0:
                            #Start timer
                            start_time = time.time()
                            start_times[question_object.index] = start_time

                        started[question_object.index] = 1
                        
    
        #--Blit Images--#
                        
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

    #---------------Testing Page---------------#

    #--Obtain Info--#

    if game_status[0] == 1:
        this_question_set = all_question_sets[game_status[1]]
        question_number = game_status[2]
        number_of_questions = len(this_question_set)
        this_question = this_question_set[question_number]
        submitted_status = submitted[game_status[1]]

        #--Create / Update icon set--#
        question_icon_set = []
        for question in this_question_set:
            this_question_index = this_question_set.index(question)
            
            in_page_index = (this_question_index) % (question_icon_columns * question_icon_rows) #start from 0
            row_number = int(in_page_index / question_icon_columns)  #start from 0
            column_number = in_page_index % question_icon_columns  #start from 0
            
            position_x = question_icon_padx + column_number * (question_icon_marginx + question_icon_width)
            position_y = question_icon_top_displacement + row_number * (question_icon_marginy + question_icon_height)
            new_question_icon = QuestionIcon(question, this_question_index, position_x, position_y)
            
            question_icon_set.append(new_question_icon)


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()


                #--In unsubmitted mode, allow user to select choices--#
                if submitted_status == 0:
                    for choice in this_question.choices:
                        if choice.box_position.collidepoint(mouse_position):
                            index = this_question.choices.index(choice)
                            choice.selected = -choice.selected
                            this_question.choices[index] = choice

                            if choice.selected == 1:
                                this_question.chosen = 1
                                if choice.correct == 1:
                                    this_question.correct = 1
                                choice.refresh_picture(choice_box_selected_image)
                                
                            if choice.selected == -1:
                                this_question.chosen = 0
                                this_question.correct = 0
                                choice.refresh_picture(choice_box_image)

                            this_question_set[question_number] = this_question
                            
                            #Only supports single choice
                            for other_choice in this_question.choices:
                                if other_choice != choice:
                                    other_index = this_question.choices.index(other_choice)
                                    other_choice.selected = -1      
                                    other_choice.refresh_picture(choice_box_image)      
                                    this_question.choices[other_index] = other_choice
                                    this_question_set[question_number] = this_question

                            break

                #--Flip page--#
                if nextpage_position.collidepoint(mouse_position):
                    game_status = [game_status[0],game_status[1],game_status[2]+1,0]
                    
                if previouspage_position.collidepoint(mouse_position):
                    game_status = [game_status[0],game_status[1],game_status[2]-1,0]

                if game_status[2] >= number_of_questions:
                    game_status = [game_status[0],game_status[1],number_of_questions-1,0]
                if game_status[2] < 0:
                    game_status = [game_status[0],game_status[1],0,0]

                #--Return to homepage--#
                if return_position.collidepoint(mouse_position):
                    game_status = [0,0,0,0]

                #--Star this question--#
                if star_position.collidepoint(mouse_position):
                    this_question.starred = -this_question.starred
                    this_question_set[question_number] = this_question
                #--Go to mainpage--#
                if mainpage_position.collidepoint(mouse_position):
                    game_status = [2,game_status[1],game_status[2],0]

                    

        if submitted_status == 1:
            #--Blit "unattempted" sign when submitted--#
            if this_question.chosen == 0:
                screen.blit(unattempted_image, unattempted_position)

            #--Refresh choice box pictures after submission--#
            for choice in this_question.choices:
                if choice.selected == 1 and choice.correct == 1:
                    choice.refresh_picture(choice_box_correct_image)
                if choice.selected == 1 and choice.correct == 0:
                    choice.refresh_picture(choice_box_wrong_image)
                if this_question.chosen == 0 and choice.correct == 1:
                    choice.refresh_picture(choice_box_correct_unselected_image)

                this_question_set[question_number] = this_question

        this_question.blit_question()

        #--Blit all images--#
        screen.blit(nextpage_image, nextpage_position)
        screen.blit(previouspage_image, previouspage_position)
        screen.blit(return_image, return_position)
        screen.blit(mainpage_image, mainpage_position)

        if this_question.starred == -1:
            screen.blit(star_image, star_position)
        if this_question.starred == 1:
            screen.blit(selected_star_image, selected_star_position)

        pygame.display.flip()
        screen.fill((255,255,255))


    #---------------Main Page---------------#
    
    if game_status[0] == 2:
        screen.blit(mainpage_background_image, mainpage_background_position)

        
        mainpage_page_number = game_status[3]
        question_icon_every_page = (question_icon_columns * question_icon_rows)

        if len(question_icon_set) / (question_icon_every_page) == int(len(question_icon_set) / (question_icon_every_page)):
            total_page_number = len(question_icon_set) / (question_icon_every_page)
        else:
            total_page_number = int(len(question_icon_set) / (question_icon_every_page)) + 1

        #--Get info for this page--#
        mainpage_start_index = mainpage_page_number * (question_icon_columns * question_icon_rows) 
        mainpage_end_index_1 = (mainpage_page_number+1) * (question_icon_columns * question_icon_rows) - 1
        mainpage_end_index_2 = len(question_icon_set) - 1
        mainpage_end_index = min(mainpage_end_index_1, mainpage_end_index_2)
        this_question_icon_set = question_icon_set[int(mainpage_start_index) : int(mainpage_end_index) + 1]
        this_time_used = times[game_status[1]]
            

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                for question_icon in this_question_icon_set:
                    if question_icon.question_icon_position.collidepoint(mouse_position):
                        game_status = [1, game_status[1], question_icon.index,0]


                #--Flip page--#

                if nextpage_position.collidepoint(mouse_position):
                    game_status = [2, game_status[1], game_status[2], game_status[3]+1]
                if previouspage_position.collidepoint(mouse_position):
                    game_status = [2, game_status[1], game_status[2], game_status[3]-1]

                if game_status[3] >= total_page_number:
                    game_status = [game_status[0], game_status[1], game_status[2], total_page_number -1]
                if game_status[3] < 0:
                    game_status = [game_status[0], game_status[1], game_status[2], 0]

                #--Return to testing page--#
                if return_position.collidepoint(mouse_position):
                    game_status = [1, game_status[1], game_status[2], 0]


                
                #--Submit answers--#
                if submit_position.collidepoint(mouse_position):
                    if submitted[game_status[1]] == 0:
                        end_time = time.time()
                        this_start_time = start_times[game_status[1]]
                        time_used = round(end_time - this_start_time, 2)
                        times[game_status[1]] = time_used
                        time.sleep(1)

                    
                    submitted[game_status[1]] = 1 #change submitted status 
                    
                    correct_count = 0
                    wrong_count = 0
                    for question in this_question_set:
                        if question.correct == 1:
                            correct_count += 1
                        if question.correct == 0:
                            wrong_count += 1

                    correct_counts[game_status[1]] = correct_count
                    wrong_counts[game_status[1]] = wrong_count
                    
                    score = round(correct_count / len(this_question_set), 2) * 100
                    scores[game_status[1]] = score

        #--Get score, time info and create fonts--#
        current_score = scores[game_status[1]]
        current_time = times[game_status[1]]
        current_correct_count = correct_counts[game_status[1]]
        current_wrong_count = wrong_counts[game_status[1]]
        
        result_font = pygame.font.Font(None, result_font_value)
        text_1 = "Total Questions: " + str(len(this_question_set)) + ", Correct: " + str(current_correct_count) + ", Wrong: " + str(current_wrong_count)
        text_2 = "Score: " + str(current_score) + "%, Time Used: " + str(current_time)+ " seconds"
        
        result_text_1 = result_font.render(text_1, True, result_color)
        result_text_position_1 = result_text_1.get_rect()
        result_text_position_1.center = screen_width/2, result_first_displacement
        
        result_text_2 = result_font.render(text_2, True, result_color)
        result_text_position_2 = result_text_2.get_rect()
        result_text_position_2.center = screen_width/2, result_second_displacement

        
        #-----Blitting Images-----#
        
        #--Blit question icons according to submission status--#
        for question_icon in this_question_icon_set:
            if submitted[game_status[1]] == 0:
                question_icon.blit_questionicon()
            if submitted[game_status[1]] == 1:
                question_icon.blit_submitted_icon()

        #--Blit results if submitted--#
        if submitted[game_status[1]] == 1:
            screen.blit(result_text_1, result_text_position_1)
            screen.blit(result_text_2, result_text_position_2)

        #--Blit other images--#
        screen.blit(nextpage_image, nextpage_position)
        screen.blit(previouspage_image, previouspage_position)
        screen.blit(return_image, return_position)
        screen.blit(submit_image, submit_position)
        
        pygame.display.flip()
        screen.fill((255,255,255))
