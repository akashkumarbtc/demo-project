from django.db.models import Q
from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView  
from rest_framework.throttling import ScopedRateThrottle 
from external_apis_app.serializers import ContextSerializer
from admin_panel_app.app.permissions import HasGroupPermission
from chatbot_app.models import Context, Answers, Document, FocusAddress, BranchAdress


class QuestionListView(ListAPIView):
    permission_classes = [HasGroupPermission]
    required_groups    = ["External",]
    throttle_classes   = [ScopedRateThrottle]
    throttle_scope     = 'question-list-throttle'
    queryset           = Context.objects.all().order_by('context_name')
    serializer_class   = ContextSerializer


class ContextDetailView(APIView):
    permission_classes = [HasGroupPermission]
    required_groups    = ["External",]
    throttle_classes   = [ScopedRateThrottle]
    throttle_scope     = 'context-list-throttle'
    
    def post(self, request, format=None):
        """
        Post method to retrieve context details.
        """
        last_updated_date  = request.data.get('last_updated_date')
        fetch_all          = request.data.get('fetch_all')

        response = []
        if last_updated_date and int(fetch_all) == 0:
            # fetch only the records updated after the last_updated_date
            all_nodes = Answers.objects.select_related('context_id', 'document') \
            .filter(Q(updated_at__date__gte=last_updated_date) | Q(created_at__date__gte=last_updated_date)).order_by('context_id__context_name')
        else:
            # fetch all the records.
            all_nodes = Answers.objects.select_related('context_id', 'document').order_by('context_id__context_name')

        for node in all_nodes:
            doc_url = node.document.document.url if node.document else None
            obj = {
                "uuid": node.context_id.uuid,
                "question": node.context_id.context_name,
                "answer": node.answer,
                "document": doc_url,
                "updated_at": node.updated_at
            }
            response.append(obj)

        return Response(response,status=200)


class FocusAddressView(APIView):
    permission_classes = [HasGroupPermission]
    required_groups    = ["External",]
    throttle_classes   = [ScopedRateThrottle]
    throttle_scope     = 'question-list-throttle'

    data = {
        "Public Issues": '''<a href="/" rel="noopener noreferrer" target="_blank">Email-Public-Issues</a>''',
        "R and T": '''<a href="/" rel="noopener noreferrer" target="_blank">Email-R-T</a>''',
        "Bonds": '''<a href="/" rel="noopener noreferrer" target="_blank">Email-Bonds</a>''',
        "Focus Address": '''<a href="/" rel="noopener noreferrer" target="_blank">Focus Address</a>'''
    }

    def get(self, request):
        """
        Get the focus addresses and construct the response.
        """
        response = defaultdict(list)
        all_addr = {}
        
        # Fetch all the data from FocusAddress table
        focus_addr = FocusAddress.objects.values_list('company_id__name', 'topic', 'focus_answer', 'contact_info')
        
        for company_name, topic, focus_answer, contact_info in focus_addr:
            if company_name not in response:
                response[company_name].append({"keyword": self.data["Focus Address"], "value": focus_answer})
            response[company_name].append({"keyword": self.data.get(topic), "value": contact_info})
        
        # Fetch all the data from BranchAdress table
        branch_addr = BranchAdress.objects.values_list('company__name', 'branch_name', 'total_address', 'g_maps_link')

        for company_name, branch, total_address, g_maps in branch_addr:
            response[company_name].append({"keyword": f"__Total__Address-{branch.capitalize()}", "value": total_address, "g_maps": g_maps })
            if company_name not in all_addr: all_addr[company_name] = ""
            all_addr[company_name] += f'<div class="popup"><strong>{branch}</strong></div><div class="popup">{total_address}</div><p> <br/></p>'
        
        # For each company, combine all the branch addresses in one key.
        for key in all_addr:
            response[key].append({"keyword": f"__Total__Address-All", "value": all_addr[key] })

        
        return Response(dict(response), status=200)
