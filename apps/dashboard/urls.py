from .views import *
from django.urls import path

urlpatterns = [
    path('',DashView.as_view(),name='dashboards'),
    path('dashboard',HomeView.as_view(),name='dashboard'),
    path('ag',ag,name='ag'),
    path('cir',cir,name='cir'),
    path('ans', AnalyseQuantitativeView.as_view(), name='ans'),
    path('grouped-bar-chart-data/', GroupedBarChartView.as_view(), name='grouped_bar_chart_data'),
    path('ans_t/<int:pk>/detail', AnalyseQuantitativeTechnicienDetailView.as_view(), name='ans_t'),
    path('technicien/<int:pk>/analytics/', TechnicienAnalyticsView.as_view(), name='technicien-analytics-view'),
    #path('technicien-task-history/<int:technicien_id>/', TechnicienTaskHistoryView.as_view(), name='technicien_task_history'),

#    path('chart', line_chart, name='line_chart'),
#    path('chartJSON', line_chart_json, name='line_chart_json'),
]


