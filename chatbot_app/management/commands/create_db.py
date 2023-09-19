from django.core.management.base import BaseCommand, CommandError
import uuid

from chatbot_app.models import BranchAdress,Context,Answers,Frequency,Tag


class Command(BaseCommand):
    help = 'Adds basic required data in database'

    def handle(self, *args, **kwargs):
        BranchAdress.objects.create_BranchAdress('linkintime','MUMBAI','179-1','''Link Intime India Pvt. Ltd - MUMBAI,
C 101, 247 Park, L.B.S.Marg, Vikhroli (West), Mumbai - 400083.
''','1800 1020 878','mumbai@linkintime.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >Link Intime India Pvt. Ltd - Mumbai,</strong>
</p>
<p>
    <span >C 101, 247 Park, L.B.S.Marg, Vikhroli (West), Mumbai - 400083.</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:rnt.helpdesk@linkintime.co.in" target="_blank" >rnt.helpdesk@linkintime.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91- 022 - 4918 6270</span>
</p>''')

        BranchAdress.objects.create_BranchAdress('linkintime','MUMBAI','189-1','''Link Intime India Pvt. Ltd,
C 101, 247 Park, L.B.S.Marg, Vikhroli (West), Mumbai - 400083.
''','1800 1020 878','mumbai@linkintime.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >Link Intime India Pvt. Ltd - Mumbai,</strong>
</p>
<p>
    <span >C 101, 247 Park, L.B.S.Marg, Vikhroli (West), Mumbai - 400083.</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:rnt.helpdesk@linkintime.co.in" target="_blank" >rnt.helpdesk@linkintime.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91- 022 - 4918 6270</span>
</p>''')
        BranchAdress.objects.create_BranchAdress('linkintime','AHMEDABAD','185-1','''Link Intime India Pvt. Ltd - AHMEDABAD,
5 th  Floor, 506 TO 508,Amarnath Business Centre – 1 ( ABC-1),
Beside Gala Business Centre,Nr. St. Xavier’s College Corner,
Off C G Road, Ellisbridge, Ahmedabad - 380006.
''','079 - 2646 5179','ahmedabad@linkintime.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >Link Intime India Pvt. Ltd - AHMEDABAD,</strong>
</p>
<p>
    <span >5 th  Floor, 506 TO 508,Amarnath Business Centre – 1 ( ABC-1),
Beside Gala Business Centre,Nr. St. Xavier’s College Corner,
Off C G Road, Ellisbridge, Ahmedabad - 380006.</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:ahmedabad@linkintime.co.in" target="_blank" >ahmedabad@linkintime.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-079- 2646 5179</span>
</p>''')

        BranchAdress.objects.create_BranchAdress('linkintime','COIMBATORE','187-1','''Link Intime India Pvt. Ltd - COIMBATORE,
Surya 35, Mayflower Avenue,
Behind Senthil Nagar, Sowripalayam Road,
Coimbatore - 641028.
''','0422 - 2314 792','coimbatore@linkintime.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >Link Intime India Pvt. Ltd - COIMBATORE,</strong>
</p>
<p>
    <span >Surya 35, Mayflower Avenue,
Behind Senthil Nagar, Sowripalayam Road,
Coimbatore - 641028.</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:coimbatore@linkintime.co.in" target="_blank" >coimbatore@linkintime.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-0422 - 2314 792</span>
</p>''')

        BranchAdress.objects.create_BranchAdress('linkintime','KOLKATA','181-1','''Link Intime India Pvt. Ltd - KOLKATA,
Vaishno Chamber, 5 th  Floor, Flat Nos-502 &amp; 503
6, Brabourne Road, Kolkata - 700 001.
''','+91-033 4004 9728 / 033-4073 1698','kolkata@linkintime.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >Link Intime India Pvt. Ltd - KOLKATA,</strong>
</p>
<p>
    <span >Vaishno Chamber, 5 th  Floor, Flat Nos-502 &amp; 503
6, Brabourne Road, Kolkata - 700 001.</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:kolkata@linkintime.co.in" target="_blank" >kolkata@linkintime.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-033 4004 9728 / 033-4073 1698</span>
</p>''')

        BranchAdress.objects.create_BranchAdress('linkintime','NEW DELHI','183-1','''Link Intime India Pvt. Ltd - NEW DELHI,
Noble Heights, 1 st  floor, Plot No NH-2, C-1 Block, LSC,
Near Savitri Market, Janakpuri,New Delhi - 110058
''','+91-011-4141 0592 /93 /94','delhi@linkintime.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >Link Intime India Pvt. Ltd - NEW DELHI,</strong>
</p>
<p>
    <span >Noble Heights, 1 st  floor, Plot No NH-2, C-1 Block, LSC,
Near Savitri Market, Janakpuri,New Delhi - 110058</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:delhi@linkintime.co.in" target="_blank" >delhi@linkintime.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-011-4141 0592 /93 /94</span>
</p>''')

        Context.objects.create_context('Our Branch Address',uuid.uuid4(), uuid.uuid4(), True, False)
        Answers.objects.create_answers(Context.objects.get(context_name='Our Branch Address'),
                                       '''OUR BRANCH LOCATIONS
__Total__Address-All''',
                                       None,
                                       None)
        Tag.objects.create_tags(Context.objects.get(
            context_name='Our Branch Address'), ['our branch address', 'all branch', "all branches", "branch locator"])

        Context.objects.create_context('Mumbai Address',uuid.uuid4(), uuid.uuid4(), True, False)
        Answers.objects.create_answers(Context.objects.get(context_name='Mumbai Address'),
                                       '''Mumbai Banch Address
__Total__Address-Mumbai''',
                                       None,
                                       None)
        Tag.objects.create_tags(Context.objects.get(
            context_name='Mumbai Address'), ['mumbai branch address'])
        
        Context.objects.create_context('Ahmedabad Address',uuid.uuid4(), uuid.uuid4(), True, False)
        Answers.objects.create_answers(Context.objects.get(context_name='Ahmedabad Address'),
                                       '''Ahmedabad Banch Address
__Total__Address-Ahmedabad''',
                                       None,
                                       None)
        Tag.objects.create_tags(Context.objects.get(
            context_name='Ahmedabad Address'), ['Ahmedabad branch address'])

        Context.objects.create_context('Coimbatore Address',uuid.uuid4(), uuid.uuid4(), True, False)
        Answers.objects.create_answers(Context.objects.get(context_name='Coimbatore Address'),
                                       '''Coimbatore Banch Address
__Total__Address-Coimbatore''',
                                       None,
                                       None)
        Tag.objects.create_tags(Context.objects.get(
            context_name='Coimbatore Address'), ['Coimbatore branch address'])

        Context.objects.create_context('Kolkata Address',uuid.uuid4(), uuid.uuid4(), True, False)
        Answers.objects.create_answers(Context.objects.get(context_name='Kolkata Address'),
                                       '''Kolkata Banch Address
__Total__Address-Kolkata''',
                                       None,
                                       None)
        Tag.objects.create_tags(Context.objects.get(
            context_name='Kolkata Address'), ['Kolkata branch address'])

        Context.objects.create_context('New Delhi Address',uuid.uuid4(), uuid.uuid4(), True, False)
        Answers.objects.create_answers(Context.objects.get(context_name='New Delhi Address'),
                                       '''New Delhi Banch Address
__Total__Address-New Delhi''',
                                       None,
                                       None)
        Tag.objects.create_tags(Context.objects.get(
            context_name='New Delhi Address'), ['New Delhi branch address'])
        
        Context.objects.create_context('Pune Address',uuid.uuid4(), uuid.uuid4(), True, False)
        Answers.objects.create_answers(Context.objects.get(context_name='Pune Address'),
                                       '''Pune Banch Address
__Total__Address-Pune''',
                                       None,
                                       None)
        Tag.objects.create_tags(Context.objects.get(
            context_name='Pune Address'), ['Pune branch address'])
        
        Context.objects.create_context('Vadodara Address',uuid.uuid4(), uuid.uuid4(), True, False)
        Answers.objects.create_answers(Context.objects.get(context_name='Vadodara Address'),
                                       '''Vadodara Banch Address
__Total__Address-Vadodara''',
                                       None,
                                       None)
        Tag.objects.create_tags(Context.objects.get(
            context_name='Vadodara Address'), ['Vadodara branch address'])
        
        Context.objects.create_context('Bangalore Address',uuid.uuid4(), uuid.uuid4(), True, False)
        Answers.objects.create_answers(Context.objects.get(context_name='Bangalore Address'),
                                       '''Bangalore Banch Address
__Total__Address-Bangalore''',
                                       None,
                                       None)
        Tag.objects.create_tags(Context.objects.get(
            context_name='Bangalore Address'), ['Bangalore branch address'])
        
        Context.objects.create_context('Jamshedpur Address',uuid.uuid4(), uuid.uuid4(), True, False)
        Answers.objects.create_answers(Context.objects.get(context_name='Jamshedpur Address'),
                                       '''Jamshedpur Banch Address
__Total__Address-Jamshedpur''',
                                       None,
                                       None)
        Tag.objects.create_tags(Context.objects.get(
            context_name='Jamshedpur Address'), ['Jamshedpur branch address'])
        
        BranchAdress.objects.create_BranchAdress('linkintime','PUNE','180-1','''Link Intime India Pvt. Ltd - PUNE,
Block No. 202,
2nd Floor, Akshay Complex,
Near Ganesh Temple,
Off Dhole Patil Road,
Pune - 411001.
''','+91-020 -4601 4473','pune@linkintime.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >Link Intime India Pvt. Ltd - PUNE,</strong>
</p>
<p>
    <span >Block No. 202,
2nd Floor, Akshay Complex,
Near Ganesh Temple,
Off Dhole Patil Road,
Pune - 411001.</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:pune@linkintime.co.in" target="_blank" >pune@linkintime.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-020 -4601 4473</span>
</p>''')
        BranchAdress.objects.create_BranchAdress('linkintime','VADODARA','184-1','''Link Intime India Pvt. Ltd - VADODARA,
Shangrila Complex,1 st  Floor,Opp. HDFC Bank,
B Tower, 102 B and 103, Near Radhakrishna Char Rasta,
Akota, Vadodara 390020.
''','+91-0265 - 6136000','vadodara@linkintime.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >Link Intime India Pvt. Ltd - VADODARA,</strong>
</p>
<p>
    <span >Shangrila Complex,1 st  Floor,Opp. HDFC Bank,
B Tower, 102 B and 103, Near Radhakrishna Char Rasta,
Akota, Vadodara 390020.</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:vadodara@linkintime.co.in" target="_blank" >:vadodara@linkintime.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-0265 - 6136000</span>
</p>''')

        BranchAdress.objects.create_BranchAdress('linkintime','VADODARA','194-1','''Link Intime India Pvt. Ltd - VADODARA,
Shangrila Complex,1 st  Floor,Opp. HDFC Bank,
B Tower, 102 B and 103, Near Radhakrishna Char Rasta,
Akota, Vadodara 390020.
''','+91-0265 - 6136000','vadodara@linkintime.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >Link Intime India Pvt. Ltd - VADODARA,</strong>
</p>
<p>
    <span >Shangrila Complex,1 st  Floor,Opp. HDFC Bank,
B Tower, 102 B and 103, Near Radhakrishna Char Rasta,
Akota, Vadodara 390020.</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:vadodara@linkintime.co.in" target="_blank" >:vadodara@linkintime.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-0265 - 6136000</span>
</p>''')

        BranchAdress.objects.create_BranchAdress('tcplindia','MUMBAI','190-1','''TSR Consultants Private Limited - MUMBAI
C 101, 1 st  Floor, 247 Park, L.B.S.Marg, Vikhroli (West), Mumbai - 400083.
Contact Person : Ms. Supriya Mirashi / Ms. Smita Rao
''','+91-022 8108118484','csg-unit@tcplindia.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >TSR Consultants Private Limited - MUMBAI,</strong>
</p>
<p>
    <span >Noble Heights, 1 st  floor, Plot No NH-2, C-1 Block, LSC,
Near Savitri Market, Janakpuri,New Delhi - 110058</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:csg-unit@tcplindia.co.in" target="_blank" >csg-unit@tcplindia.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-022 8108118484</span>
</p>''')
        BranchAdress.objects.create_BranchAdress('tcplindia','AHMEDABAD','190-2','''TSR Consultants Private Limited - AHMEDABAD
C/o Link Intime India Private Limited
Amarnath Business Centre-1 (ABC-1)
Beside Gala Business Centre, Nr. St. Xavier&#39;s College Corner
Off. C.G. Road, Ellisbridge, Ahmedabad - 380006
''','+91-079 -2646 5179','csg-unit@tcplindia.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >TSR Consultants Private Limited - AHMEDABAD,</strong>
</p>
<p>
    <span >C/o Link Intime India Private Limited
Amarnath Business Centre-1 (ABC-1)
Beside Gala Business Centre, Nr. St. Xavier&#39;s College Corner
Off. C.G. Road, Ellisbridge, Ahmedabad - 380006</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:csg-unit@tcplindia.co.in" target="_blank" >csg-unit@tcplindia.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-079 -2646 5179</span>
</p>''')
        
        BranchAdress.objects.create_BranchAdress('tcplindia','BANGALORE','190-3','''TSR Consultants Private Limited - BANGALORE
C/o. Mr. D. Nagendra Rao,
“Vaghdevi” 543/A, 7 th  Main, 3 rd  Cross, Hanumanthnagar
Bengaluru – 560019
''','+91-080 -2650 9004','csg-unit@tcplindia.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >TSR Consultants Private Limited - BANGALORE</strong>
</p>
<p>
    <span >C/o. Mr. D. Nagendra Rao,
“Vaghdevi” 543/A, 7 th  Main, 3 rd  Cross, Hanumanthnagar
Bengaluru – 560019</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:csg-unit@tcplindia.co.in" target="_blank" >csg-unit@tcplindia.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-080 -2650 9004</span>
</p>''')
        
        BranchAdress.objects.create_BranchAdress('tcplindia','JAMSHEDPUR','190-4','''TSR Consultants Private Limited - JAMSHEDPUR
Bungalow No. 1, &#39;E&#39; Road, Northern Town Bistupur,
Jamshedpur - 831001
''','+91-657 -2426 937','csg-unit@tcplindia.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >TSR Consultants Private Limited - JAMSHEDPUR</strong>
</p>
<p>
    <span >TSR Consultants Private Limited
Bungalow No. 1, &#39;E&#39; Road, Northern Town Bistupur,
Jamshedpur - 831001</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:csg-unit@tcplindia.co.in" target="_blank" >csg-unit@tcplindia.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-657 -2426 937</span>
</p>''')
        
        BranchAdress.objects.create_BranchAdress('tcplindia','KOLKATA','190-5','''TSR Consultants Private Limited - KOLKATA
C/o Link Intime India Private Limited,
Vaishno Chamber, Flat No. 502 &amp; 503
5 th  Floor, 6, Brabourne Road, Kolkata - 700001''','+91-033 -4008 1986','csg-unit@tcplindia.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >TSR Consultants Private Limited - KOLKATA</strong>
</p>
<p>
    <span >C/o Link Intime India Private Limited,
Vaishno Chamber, Flat No. 502 &amp; 503
5 th  Floor, 6, Brabourne Road, Kolkata - 700001</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:csg-unit@tcplindia.co.in" target="_blank" >csg-unit@tcplindia.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-033 -4008 1986</span>
</p>''')
        
        BranchAdress.objects.create_BranchAdress('tcplindia','NEW DELHI','190-5','''TSR Consultants Private Limited - NEW DELHI
C/o Link Intime India Private Limited
Noble Heights, 1 st  Floor, Plot No NH-2, C-1 Block, LSC,
Near Savitri Market, Janakpuri, New Delhi – 110058''','+91-011 -4941 1030','csg-unit@tcplindia.co.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >TSR Consultants Private Limited - NEW DELHI</strong>
</p>
<p>
    <span >C/o Link Intime India Private Limited
Noble Heights, 1 st  Floor, Plot No NH-2, C-1 Block, LSC,
Near Savitri Market, Janakpuri, New Delhi – 110058</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:csg-unit@tcplindia.co.in" target="_blank" >csg-unit@tcplindia.co.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-011 -4941 1030</span>
</p>''')
        
        BranchAdress.objects.create_BranchAdress('unisec','MUMBAII','193-1','''Universal Capital Securities Pvt. Ltd - MUMBAI.
C 101, 247 Park, LBS Road, Vikhroli West, Mumbai – 400083.''','+91-022- 28207203-05, 49186178-79','info@unisec.in','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >Universal Capital Securities Pvt. Ltd - MUMBAI</strong>
</p>
<p>
    <span >C 101, 247 Park, LBS Road, Vikhroli West, Mumbai – 400083.</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:info@unisec.in" target="_blank" >info@unisec.in</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-022- 28207203-05, 49186178-79</span>
</p>''')
        
        BranchAdress.objects.create_BranchAdress('skdc-consultants','COIMBATORE','195-1','''S.K.D.C. Consultants Limited,
Surya 35,Mayflower Avenue,
Behind Senthil Nagar, Sowripalayam Road,
Coimbatore - 641028.
5 th  Floor, 6, Brabourne Road, Kolkata - 700001''','+91-422 -4958995, 2539835-36','info@skdc-consultants.com','''<p>
    <i class="fa-solid fa-location-dot"></i><strong >Link Intime India Pvt. Ltd - KOLKATA,</strong>
</p>
<p>
    <span >S.K.D.C. Consultants Limited,
Surya 35,Mayflower Avenue,
Behind Senthil Nagar, Sowripalayam Road,
Coimbatore - 641028.</span>
</p>
<p>
    <br>
</p>
<p>
    <strong >Contact Information:</strong>
</p>
<p>
    <i class="fa-solid fa-envelope"></i><span >Email :</span>
    <a href="mailto:info@skdc-consultants.com" target="_blank" >info@skdc-consultants.com</a>
</p>
<p>
    <i class="fa-solid fa-phone"></i><span >Call-us : +91-422 -4958995, 2539835-36</span>
</p>''')
        
        print('data added to DB..!')