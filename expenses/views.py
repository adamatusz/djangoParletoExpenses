from django.http import request
from django.views.generic.list import ListView
from django.shortcuts import render

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import (summary_per_category,
                      summary_per_year_month,
                      total_exp)

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 7

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            category = form.cleaned_data.get('category', )
            asc_date = form.cleaned_data.get('date_ascending',)
            des_date = form.cleaned_data.get('date_descending',)
            from_date = form.cleaned_data.get('from_date',)
            to_date = form.cleaned_data.get('to_date',)

            if name:
                queryset = queryset.filter(name__icontains=name)
            if category:
                queryset = queryset.filter(category=category)
            if asc_date:
                queryset = queryset.filter().order_by('date')
            if des_date:
                queryset = queryset.filter().order_by('-date')
            if from_date and to_date:
                queryset = queryset.filter(date__range=(from_date, to_date))
            if from_date is None and to_date:
                queryset = queryset.filter(date__lte=to_date)
            if from_date and to_date is None:
                queryset = queryset.filter(date__gte=from_date)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_per_year_month=summary_per_year_month(queryset),
            total_exp=total_exp(queryset),
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get(self, request, **kwargs):
        categories = Category.objects.all()
        expenses = Expense.objects.all()
        detail_expenses = {category.name: 0 for category in categories}
        for expense in expenses:
            detail_expenses[expense.category.name] += 1

        return render(request, 'expenses/category_list.html',
                      context={'categories': categories,
                               'detail_expenses': detail_expenses
                               })
