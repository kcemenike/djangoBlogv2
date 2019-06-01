from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView

from django.http import Http404

# Create your views here.
from .models import Product

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     # print(context)
    #     return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "products/list.html", context)




class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(id=pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance

    # We can also use the get_queryset instead of the get_object method
    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(id=pk)

def product_detail_view(request, pk=None, *args, **kwargs): #, *args, **kwargs):
    # print(args, kwargs)
    # print(pk)
    # queryset = Product.objects.all()

    # Methods to get the object with a particular key are
    # 1
    # instance = Product.objects.get(pk=pk) # pk is the primary key of every django object
    
    # 2
    # instance = get_object_or_404(Product, pk=pk)

    # 3
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print("No product here")
    #     raise Http404("Product doesn't exist")
    # except:
    #     print("huh?")

    # 4
    # qs = Product.objects.filter(id=pk)
    # print(qs)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesn't exist")

    # 5 Custom Model Manager
    instance = Product.objects.get_by_id(id=pk)
    if instance is None:
        raise Http404("Product doesn't exist")
    print(instance)

    context = {
        "object": instance
    }
    return render(request, "products/detail.html", context)

class ProductFeaturedListView(ListView):
    template_name = 'products/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all().featured()

    template_name = 'products/featured-detail.html'

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.featured()

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        # instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found...")
        except Product.MutipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("???")

        return instance