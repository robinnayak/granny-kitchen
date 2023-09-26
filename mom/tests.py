from django.test import TestCase

# Create your tests here.


#views moms
# def ProfileView(request):
#     if request.user.is_authenticated == True:
#         email = request.user.email
#         # print("userid ", email)
#         mom_obj = MomModel.objects.get(email=email)
#         menu_obj = mom_obj.momsmenu.all()
#         # try:
#         #     counts = MomModel.objects.annotate(
#         #         menuitem_count = Count('momsmenu')
#         #     )
#         #     for count in counts:
#         #         print("count ", count.menuitem_count)
#         #     print("counts ",counts)
#         # except Exception as e:
#         #     print("error",e)
#         # for menus in menu_obj:
#         #     menuitem_obj = MenuItem.objects.filter(menu__id = menus.id,menu__moms__user = request.user.username)
#         #     menuitem_obj = MenuItem.objects.filter(id=menus.id)
#         #     menuitem_obj = MenuItem.objects.filter(menu__id = menus.id)
#         #     print("menuitem ", menus.id) 
#         #     print("menuitem ", menuitem_obj) 
#         context = {"name":"profile","mom":mom_obj,"menus":menu_obj}
#         return render(request,"profile.html",context)
#     else:
#         return redirect('login')


# def ProfileView(request):
#     if request.user.is_authenticated == True:
#         item = []
#         email = request.user.email
#         # print("userid ", email)
#         mom_obj = MomModel.objects.get(email=email)
#         menu_obj = mom_obj.momsmenu.all()
#         # for menu in menu_obj:
#         #     items = MenuItem.objects.filter(menu_id=menu.id)
        
#         for menu in menu_obj:
#             items = Menu.objects.get(name=menu.name)
#             count = items.menu.count()
#             item.append(count)
#         print("count :" ,item)
#         context = {"name":"profile","mom":mom_obj,"menus":menu_obj, "itemscount":item}
#         return render(request,"profile.html",context)
#     else:
#         return redirect('login')
# def ProfileView(request):
#     if request.user.is_authenticated == True:
#         item = []
#         email = request.user.email
#         # print("userid ", email)
#         mom_obj = MomModel.objects.get(email=email)
#         menu_obj = mom_obj.momsmenu.all()
#         # for menu in menu_obj:
#         #     items = MenuItem.objects.filter(menu_id=menu.id)
        
#         for menu in menu_obj:
#             items = Menu.objects.get(name=menu.name)
#             count = items.menu.count()
#             item.append(count)
#         print("count :" ,item)
#         context = {"name":"profile","mom":mom_obj,"menus":menu_obj, "itemscount":item}
#         return render(request,"profile.html",context)
#     else:
#         return redirect('login')
