from django.shortcuts import redirect

def notLogedUsers(view_func):
    def wrapper_func(request, *args, **Kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **Kwargs )
    return wrapper_func


def allowed_Users(allowredGroups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **Kwargs):
            group =None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowredGroups:
                return view_func(request, *args, **Kwargs )
            else:
                return redirect('user/')

        return wrapper_func
    return decorator

def forAdmins(view_func):

        def wrapper_func(request, *args, **Kwargs):
            group =None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group == 'admin':
                return view_func(request, *args, **Kwargs )
            if group == 'customer':
                return redirect('user/')
            if group == 'visiteur':
                return redirect('Visiteur/')
            if group == 'Front':
                return redirect('front/')  

        return wrapper_func

def forCustomer(view_func):

        def wrapper_func(request, *args, **Kwargs):
            group =None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group == 'customer':
                return view_func(request, *args, **Kwargs )
            if group == 'admin':
                return redirect('/')
            if group == 'visiteur':
                return redirect('Visiteur/') 
            if group == 'Front':
                return redirect('front/')         

        return wrapper_func


def forVisiteur(view_func):
    
        def wrapper_func(request, *args, **Kwargs):
            group =None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group == 'visiteur':
                return view_func(request, *args, **Kwargs )
            if group == 'admin':
                return redirect('/')
            if group == 'customer':
                return redirect('user/')
            if group == 'Front':
                return redirect('front/')    

        return wrapper_func



def forFront(view_func):
    
        def wrapper_func(request, *args, **Kwargs):
            group =None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group == 'Front':
                return view_func(request, *args, **Kwargs )
            if group == 'admin':
                return redirect('/')
            if group == 'customer':
                return redirect('user/')
            if group == 'visiteur':
                return redirect('Visiteur/')

        return wrapper_func