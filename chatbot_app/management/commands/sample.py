from django.core.management.base import BaseCommand, CommandError
import uuid

from chatbot_app.models import Context, Tag, Frequency, Company, Rating, Document, Conversation, Answers
from openpyxl import Workbook
# import nltk   
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Download data into excel'

    # file1 = open("C:\\Users\\akash\\OneDrive\\Desktop\\sample.txt", "w", encoding="utf-8")
    book = Workbook() 
    sheet = book.active

    def  add_data_recursively(self, data):

        for k,v in data.items():
            if(isinstance(v, list)):
                for i in v:
                    nodes = Answers.objects.select_related('context_id').filter(context_id__prev_context=str(i['uuid'])).order_by('context_id__context_name')
                    if not len(nodes):
                        continue
                    temp = {}
                    for y in nodes:
                        tag = list(Tag.objects.filter(context_id=y.context_id.uuid).values_list('tags'))
                        if tag: tag = tag[0][0][0] 
                        else: tag = ""
                        obj = {"uuid": y.context_id.uuid, "question": y.context_id.context_name, "answer": y.answer , "keywords": tag,  "url": y.url }
                        if 'children' not in temp:
                            temp['children'] = [obj]
                            continue
                        temp['children'].append(obj)
                    
                    i.update(self.add_data_recursively(temp))

        return data

    
    def loop_children(self, child_dict ,p_row):
        if isinstance(child_dict, list):
            for i in child_dict:
                if "children" not in i:
                    temp = []
                    temp.extend(p_row)
                    temp.append(str(i["question"]))
                    temp.append(str(i["uuid"]))
                    # soup = BeautifulSoup(i["answer"])
                    # temp.append(str(soup.get_text()))
                    # temp.append(str(i["keywords"]))
                    # if i["url"]not in ["", "null", None]: temp.append(str(i["url"]))
                    # temp = temp + [None] * (12-len(temp))
                    # temp.append(str(i["keywords"]))
                    # if i["url"]not in ["", "null", None]: temp.append(str(i["url"]))
                    self.sheet.append(temp)
                    # self.file1.write(str(temp))
                    

                else: 
                    p_row.append(i["question"])
                    temp = []
                    temp.extend(p_row)
                    temp.append(str(i["question"]))
                    temp.append(str(i["uuid"]))
                    # soup = BeautifulSoup(i["answer"])
                    # temp.append(str(soup.get_text()))
                    # temp.append(str(i["keywords"]))
                    # if i["url"]not in ["", "null", None]: temp.append(str(i["url"]))
                    # temp = temp + [None] * (12-len(temp))
                    # temp.append(str(i["keywords"]))
                    # if i["url"]not in ["", "null", None]: temp.append(str(i["url"]))
                    self.sheet.append(temp)
                    self.loop_children(i["children"], p_row)
                    p_row = p_row[:-1]

            


    def handle(self, *args, **kwargs):
        data = {}
        root_nodes = Answers.objects.select_related('context_id').filter(context_id__prev_context=None).order_by('context_id__context_name')

        for x in root_nodes:
            tag = list(Tag.objects.filter(context_id=x.context_id.uuid).values_list('tags'))
            if tag: tag = tag[0][0][0] 
            else: tag = ""
            obj = {"uuid": x.context_id.uuid, "question": x.context_id.context_name, "answer": x.answer, "keywords": tag, "url": x.url }

            if str(x.context_id.prev_context) in data:
                data[str(x.context_id.prev_context)].append(obj)
            else:
                data[str(x.context_id.prev_context)] = [obj]

        
        data = self.add_data_recursively(data)

        data = data['None']

        
        # self.file1.write(str(data))
        for i in data:
        # for k,v in data.items():
            if "children" in i:
                main_topic = i["question"]
                print_row = []
                print_row.append(main_topic)
                temp = []
                temp.append(str(i["question"]))
                temp.append(str(i["uuid"]))
                # soup = BeautifulSoup(i["answer"])
                # temp.append(str(soup.get_text()))
                # temp.append(str(i["keywords"]))
                # if i["url"]not in ["", "null", None]: temp.append(str(i["url"]))
                # temp = temp + [None] * (12-len(temp))
                # temp.append(str(i["keywords"]))
                # if i["url"]not in ["", "null", None]: temp.append(str(i["url"]))
                self.sheet.append(temp)
                self.loop_children(i["children"], print_row)
                # else: 
                #     if k == 'uuid': continue 
                    # self.file1.write(str(k))
                    # self.file1.write(str(v))



        # file1.write(str(data['None']))
        self.book.save("/home/ubuntu/sample1.xlsx")
        # self.book.save("C:\\Users\\akash\\OneDrive\\Desktop\\sample.xlsx")

        # self.file1.close()