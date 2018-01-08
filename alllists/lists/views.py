from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from lists.models import List
from alllists.forms import ListForm

from django.views.generic import TemplateView, ListView
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy




#def homepage_console(request, pk=None, template_name='console.html'):
def homepage_console(request, pk=None, template_name='console.html'):
	form = ListForm()
	root_items = List.objects.filter(parent=None).order_by('order_number')
	return render(request, template_name, {'form':form, 'root_items':root_items})




def create_item_from_form(request, o_n_t_s):
	f = ListForm(request.POST or None)
	if f.is_valid():
		created_item = f.save()
		created_item.order_number = o_n_t_s
		created_item.save()
	return created_item

def list_create(request, pk=None, template_name='console.html'):

	#number of items before create
	item_count_before_create = List.objects.count()

	#create item at beginning of list
	if 'create_head' in request.POST:
		reversed_item_list_before_create = List.objects.order_by('-order_number')
		#iterate through list backwards to prevent incremention from allowing two items to have the same order number even for a moment
		for index, item in enumerate(reversed_item_list_before_create):
			item.order_number = item_count_before_create - index + 1
			item.save()
		order_number_to_set = 1

	#no need to alter any other item's order number
	#set order number of item to be created to the total count after creation
	if 'create_tail' in request.POST:
		order_number_to_set = 1 + item_count_before_create

	create_item_from_form(request, order_number_to_set)
	return redirect('homepage_console')




def increment_sublist_order_numbers_for_creation(sublist):
	for item in sublist:
		item.order_number += 1
		item.save()

def count_all_descendants(ancestor):

	if ancestor.children.count() == 0:
		return 0
	else:
		descendants = 0
		for child in ancestor.children.all():
			descendants += 1 + count_all_descendants(child)
		return descendants


def list_create_child(request, pk, template_name='console.html'):

	parent_item = get_object_or_404(List, pk=pk)

	if 'create_child_head' in request.POST:
		item_list_ordered_after_child_to_create = List.objects.filter(order_number__gt=parent_item.order_number)
		order_number_to_set = parent_item.order_number + 1

	if 'create_child_tail' in request.POST:
		item_list_ordered_after_child_to_create = List.objects.filter(order_number__gt=parent_item.order_number+count_all_descendants(parent_item))
		order_number_to_set = parent_item.order_number + count_all_descendants(parent_item) + 1

	increment_sublist_order_numbers_for_creation(item_list_ordered_after_child_to_create)
	child_item = create_item_from_form(request, order_number_to_set)
	parent_item.children.add(child_item)
	parent_item.save()
	return redirect('homepage_console')



def list_delete(request, pk, template_name='console.html'):
	list = get_object_or_404(List, pk=pk)
	#form = ListForm(request.POST or None, instance=list)
	form = ListForm(None, instance=list)
	order_number_of_list_to_be_deleted = list.order_number
	if list.children.count() > 0 and list.parent.count() == 1:
		children_whose_parent_is_being_deleted_so_grandparent_will_adopt = List.objects.all().filter(order_number__gt=order_number_of_list_to_be_deleted).filter(order_number__lte=order_number_of_list_to_be_deleted+list.children.count())
		list.children.clear()
		for child in children_whose_parent_is_being_deleted_so_grandparent_will_adopt:
			list.parent.get().children.add(child)
	if request.method=='POST': #'POST' HAS TO BE CAPITALIZED, WILL NOT WORK IF LOWERCASE
		list.delete()
	lists = List.objects.all().filter(order_number__gt=order_number_of_list_to_be_deleted)
	for item in lists:
		item.order_number -= 1
		item.save()
	return redirect('homepage_console')



def has_sibling_item_above(item):

	sibling_item_above_confirmed = False
	index = item.order_number - 1

	if item.parent.count() == 0:
		while index > 0:
			if List.objects.get(order_number=index).parent.count() == 0:
				sibling_item_above_confirmed = True
				break
			index -= 1
		
	else:
		while index > item.parent.get().order_number:
			if item.parent.get() == List.objects.get(order_number=index).parent.get():
				sibling_item_above_confirmed = True
				break
			index -= 1
	
	return sibling_item_above_confirmed


#item  must not have order_number of 1 (must not be 1st item in list)
def find_nearest_item_above_of_same_level(item):
	item_above_of_same_level_index = item.order_number - 1
	if item.parent.count() == 0:
		while List.objects.get(order_number=item_above_of_same_level_index).parent.count() != 0:
			item_above_of_same_level_index -= 1
	else:
		while item.parent.get() != List.objects.get(order_number=item_above_of_same_level_index).parent.get():
			item_above_of_same_level_index -= 1
	return List.objects.get(order_number=item_above_of_same_level_index)

def list_tab(request, pk, template_name='console.html'):

	item = get_object_or_404(List, pk=pk)
	form = ListForm(None, instance=item)

	if item.order_number != 1 and has_sibling_item_above(item):
		parent_item = find_nearest_item_above_of_same_level(item)
		if(item.parent.count() != 0):
			item.parent.get().children.remove(item)
			#item.parent.get().save()
		parent_item.children.add(item)
		parent_item.save()
	return redirect('homepage_console')


def list_untab(request, pk, template_name='console.html'):

	item = get_object_or_404(List, pk=pk)
	form = ListForm(None, instance=item)

	if item.parent.count() != 0:
		for sibling in item.parent.get().children.filter(order_number__gt=item.order_number):
			item.parent.get().children.remove(sibling)
			item.children.add(sibling)
		new_parent_count = item.parent.get().parent.count()
		if new_parent_count != 0:
			new_parent_item = item.parent.get().parent.get()
		item.parent.get().children.remove(item)
		if new_parent_count != 0:
			new_parent_item.children.add(item)

	return redirect('homepage_console')




def old_list_untab(request, pk, template_name='console.html'):

	item = get_object_or_404(List, pk=pk)
	form = ListForm(None, instance=item)

	if item.parent.count() != 0:
		new_parent_count = item.parent.get().parent.count()
		if new_parent_count != 0:
			new_parent_item = item.parent.get().parent.get()
		item.parent.get().children.remove(item)
		if new_parent_count != 0:
			new_parent_item.children.add(item)

	return redirect('homepage_console')




def undo_last_action(request, template_name='console.html'):

	return redirect('homepage_console')


def nuke_it_all(request, template_name='nuke_it_all'):

	everything = List.objects.all()
	for list in everything:
		list.delete()
	return redirect('homepage_console')



	'''
	parent_item = get_object_or_404(List, pk=pk)
	form = ListForm(request.POST or None)
	if form.is_valid():
		child_list = form.save()
		parent_item.children.add(child_list)
		parent_item.save()
	return redirect('homepage_console')	
	'''


'''

some examples

def hello_HttpResponse(request):
    return HttpResponse("Hello world") 	

def hello_render(request):
	return render(request, 'hello.html') #would work if hello.html is in templates

def hello_HttpResponseRedirect(request):
	return HttpResponseRedirect('/hello/') # would work if url(r'^hello/$', views.hello_HttpResponse) was defined
'''



'''

not sure what this is at all

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form':form})

'''



'''

extra helper function + view functions

def retrieve_list_data():
	lists = List.objects.all()
	data = {}
	data['object_list'] = lists
	return data

def list_list(request, template_name='list.html'):
	data = retrieve_list_data()
	return render(request, template_name, data)

def list_create(request, template_name='4m.html'):
	form = ListForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('list_list')
	return render(request, template_name, {'form':form})

def list_update(request, pk, template_name='4m.html'):
	list = get_object_or_404(List, pk=pk)
	form = ListForm(request.POST or None, instance=list)
	if form.is_valid():
		form.save()
		return redirect('list_list')
	return render(request, template_name, {'form':form})

'''

