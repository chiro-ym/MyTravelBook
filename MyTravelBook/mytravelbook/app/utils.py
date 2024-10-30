from django.urls import reverse

def get_breadcrumb_for_travel_detail(travel_record):
    return [
        {'name': '旅行記録一覧', 'url': reverse('travel_list')},
        {'name': travel_record.title, 'url': reverse('travel_detail', args=[travel_record.id])}
    ]

def get_breadcrumb_for_category_detail(travel_record, category):
    breadcrumb = get_breadcrumb_for_travel_detail(travel_record)
    breadcrumb.append({'name': category.category_name, 'url': None})
    return breadcrumb

def get_breadcrumb_for_memo_list(travel_record):
    breadcrumb = get_breadcrumb_for_travel_detail(travel_record)
    breadcrumb.append({'name': 'たびメモ', 'url': None})
    return breadcrumb
