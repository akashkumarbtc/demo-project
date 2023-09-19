from chatbot_app.models import Context, Tag, Frequency, Company, Rating, Document, Conversation, Answers
from django.core.management.base import BaseCommand, CommandError
import csv

class Command(BaseCommand):
    help = 'Download data into excel'
    

    def handle(self, *args, **kwargs):
        file1 = open("/home/ubuntu/registry.csv", "w", encoding="utf-8")
        file2 = open("/home/ubuntu/registry_count.csv", "w", encoding="utf-8") 
        # file1 = open("C:\\Users\\akash\\OneDrive\\Desktop\\registry.csv", "w", encoding="utf-8") 
        writer = csv.writer(file1)
        writer2 = csv.writer(file2)
        data = {}
        queue = []
        main_topic = Context.objects.filter(context_name = 'Registry').values('uuid').first()['uuid']

        queue.append(main_topic)
        idx = 0

        uniq = set()

        while idx < len(queue):
            current = queue[idx]
            idx += 1


            topic = Context.objects.filter(uuid = current).first()
            answer = Answers.objects.filter(context_id=str(topic.uuid)).first()
            # tag = Tag.objects.filter(context_id=str(topic.uuid)).first()
            freq = Frequency.objects.filter(context_id=str(topic.uuid)).first()

            # doc = None

            # if str(answer.document) == 'None':
            #     doc = None
            # else: 
            #     doc = f"Document.objects.get(document='{answer.document}')"

            # context = f"Context.objects.create_context('{topic.context_name}', '{topic.uuid}', '{topic.prev_context}', {topic.leaf_node}, {topic.inputs_required})\n"
            # answers = f"Answers.objects.create_answers(Context.objects.get(uuid='{topic.uuid}'),'''{answer.answer}''',{doc},{answer.url})\n"
            # tags = f"Tag.objects.create_tags(Context.objects.get(uuid='{topic.uuid}'), {tag.tags})\n"
            # freq = f"Frequency.objects.create_frequency(Context.objects.get(uuid='{topic.uuid}'), 0)\n"

            # file1.write(context)
            # file1.write(answers)
            # file1.write(tags)
            # file1.write(freq)
            # file1.write("\n")
            focus_address = '''Focus Address'''
            email_r_t     = '''Email-R-T'''
            email_public  = '''Email-Public-Issues'''
            email_bonds   = '''Email-Bonds'''
            anchor = '''</a>'''

            ans = answer.answer
            if ans.find(focus_address) != -1:
                data = [topic.context_name, "Focus Address"]
                writer.writerow(data)
            if ans.find(email_r_t) != -1:
                data = [topic.context_name, "Email R and T"]
                writer.writerow(data)
            if ans.find(email_public) != -1:
                data = [topic.context_name, "Email Public Issues"]
                writer.writerow(data)
            if ans.find(email_bonds) != -1:
                data = [topic.context_name, "Email Bonds"]
                writer.writerow(data)
            if ans.find(anchor) != -1:
                data = [topic.context_name, "Anchor Tag"]
                writer.writerow(data)

            if topic.context_name not in uniq:
                uniq.add(topic.context_name)
                data = [topic.context_name, freq.frequency]
                writer2.writerow(data)

            all_nodes = Context.objects.filter(prev_context=topic.uuid).values('uuid').all()

            for x in all_nodes:
                queue.append(x['uuid'])
        
        
        # file1.write("\n")



        file1.close()
        file2.close()
        
                    
        