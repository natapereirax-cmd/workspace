#----------------IMPORTS--------------------
import sys
from datetime import date
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QStackedLayout,
    QTableWidget, QGraphicsDropShadowEffect, QDialog, QScrollArea,
    QButtonGroup, QLineEdit, QComboBox, QTextEdit, QDateEdit, QMainWindow, QProgressBar, QStackedWidget)
from PySide6.QtCore import Qt, QDate
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
from PySide6.QtGui import (QIcon, QPixmap, QFontDatabase, QIntValidator, QColor, QFont, QBrush)
from app.menu_style import style
from app.backend.tasks import count_tasks, count_pending_tasks, count_completed_status, count_overdue_tasks, create_task, category_statistics, get_upcoming_deadlines, get_weekly_completed_tasks, get_recent_activity, get_tasks_by_category, complete_task, delete_task
from app.backend.categories import create_category, load_categories, count_categories, delete_category

#----------------SIDEBAR--------------------
class SideBar(QFrame):
    def __init__(self, firstname, user):
        super().__init__()
        self.setStyleSheet(style())
        self.user = user

        self.setFixedSize(180, 600)
        self.bg = QLabel(self)
        self.bg.setPixmap(QPixmap('desktop_app/app/images/side_bg.png'))
        self.bg.setGeometry(0, 0, self.width(), self.height())
        self.bg.lower()

        font_id_1 = QFontDatabase.addApplicationFont('desktop_app/app/fonts/BebasNeue-Regular.ttf')
        font_id_2 = QFontDatabase.addApplicationFont('desktop_app/app/fonts/Victory Striker Sans Demo.otf')
        font_id_3 = QFontDatabase.addApplicationFont('desktop_app/app/fonts/Bebas-Regular.ttf')
        font_id_4 = QFontDatabase.addApplicationFont('desktop_app/app/fonts/CaviarDreams_Bold.ttf')

        welcome_label = QLabel(f" Welcome,\n {firstname}!")
        welcome_label.setObjectName('wlc')

        self.dashboard_btn = QPushButton('Dashboard')
        self.dashboard_btn.setFixedHeight(42)
        self.dashboard_btn.setCheckable(True)
        self.dashboard_btn.setChecked(True)

        self.categories_btn = QPushButton('Categories')
        self.categories_btn.setFixedHeight(42)
        self.categories_btn.setCheckable(True)

        self.statistics_btn = QPushButton('Statistics')
        self.statistics_btn.setFixedHeight(42)
        self.statistics_btn.setCheckable(True)

        self.about_me_btn = QPushButton('About Me')
        self.about_me_btn.setFixedHeight(42)
        self.about_me_btn.clicked.connect(self.about_me_screen)

        group = QButtonGroup(self)
        group.setExclusive(True)
        group.addButton(self.dashboard_btn)
        group.addButton(self.categories_btn)
        group.addButton(self.statistics_btn)

        buttons = [self.dashboard_btn, self.categories_btn, self.statistics_btn, self.about_me_btn]
        for btn in buttons:
            btn.setObjectName('buttons')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addSpacing(82)
        layout.addWidget(welcome_label)
        layout.addSpacing(50)
        layout.addWidget(self.dashboard_btn)
        layout.addSpacing(5)
        layout.addWidget(self.categories_btn)
        layout.addSpacing(5)
        layout.addWidget(self.statistics_btn)
        layout.addSpacing(5)
        layout.addWidget(self.about_me_btn)
        layout.addStretch()

    def about_me_screen(self):
        dialog = About_me(self.user)
        dialog.exec_()

#----------------DASHBOARD--------------------
class MetricCard(QFrame):
    def __init__(self, title, value):
        super().__init__()
        self.setStyleSheet(style())

        self.setFixedHeight(70)
        self.setObjectName('metriccard')

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(14)
        shadow.setOffset(2, 4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        v_bar = QFrame()
        v_bar.setFixedWidth(6)
        v_bar.setObjectName('v_bar')

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(18, 14, 18, 14)
        content_layout.setSpacing(6)

        self.title = QLabel(title)
        self.title.setObjectName('metric_title')

        self.value = QLabel(value)
        self.value.setObjectName('metric_value')

        content_layout.addWidget(self.title)
        content_layout.addWidget(self.value)

        main_layout.addWidget(v_bar)
        main_layout.addWidget(content)

    def update_value(self, new_value):
        self.value.setText(new_value)

class CategoryProgressCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style())

        self.setObjectName('CategoryProgressCard')

        self.setMinimumHeight(250)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(14)
        shadow.setOffset(2, 4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(self)

        title = QLabel('Category Progress')
        title.setObjectName('CategoryProgressCard_title')

        scroll = QScrollArea()
        scroll.setStyleSheet('background-color: white')
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setSpacing(15)

        scroll.setWidget(container)
        main_layout.addWidget(title)
        main_layout.addWidget(scroll)
    
    def load_data(self, data):
        self._clear_rows()

        for name, completed, pending, overdue in data:
            self.container_layout.addWidget(
                self._create_row(name, completed, pending, overdue)
            )
        
        self.container_layout.addStretch()

    def _clear_rows(self):
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def _create_row(self, name, completed, pending, overdue):
        completed = completed or 0
        pending = pending or 0
        overdue = overdue or 0

        total = completed + pending + overdue
        percent = int((completed / total) * 100) if total else 0

        row = QFrame()
        layout = QVBoxLayout(row)

        title = QLabel(name)

        progress = QProgressBar()
        progress.setValue(percent)
        
        stats = QLabel(
            f"✅ Completed: {completed} | "
            f"⚠️ Pending: {pending} | "
            f"⏰ Overdue: {overdue}"
            )
        
        stats.setObjectName('category_stats')
        
        layout.addWidget(title)
        layout.addWidget(progress)
        layout.addWidget(stats)

        return row
    
class ChartCard(QFrame):
    def __init__(self, task_backend, user_id, subtitle_font='Arial', categories_layout=None):
        super().__init__()
        self.setStyleSheet(style())

        self.task_backend = task_backend
        self.user_id = user_id
        self.subtitle_font = subtitle_font
        self.categories_layout = categories_layout

        self.setup_ui()

    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('ChartCard')

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        font_id = QFontDatabase.addApplicationFont('desktop_app/app/fonts/Bebas-Regular.ttf')
        font = QFontDatabase.applicationFontFamilies(font_id)[0]

        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(12, 12, 12, 12)

        if self.task_backend and self.user_id:
            week_data = self.task_backend(self.user_id)
        else:
            week_data = [0] * 7

        self.bar_set = QBarSet('Productivity')
        self.bar_set.append(week_data)
        self.bar_set.setColor(QColor('#161719'))
        self.bar_set.setBorderColor(Qt.transparent)

        series = QBarSeries()
        series.append(self.bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Weekly Completed Tasks')
        chart.setTitleBrush(QBrush(QColor('#161719')))

        chart_font = QFont(font, 15)
        chart.setTitleFont(chart_font)

        chart.legend().setVisible(False)

        categories = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat('%d')
        axis_y.setMin(0)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setMinimumHeight(250)
        chart_view.setStyleSheet('background: transparent;')

        card_layout.addWidget(chart_view)

    def get_widget_with_categories(self):

        layout = QHBoxLayout()

        if self.categories_layout:
            layout.addLayout(self.categories_layout)

        layout.addWidget(self)
        return layout
    def refresh_weekly_chart(self):
        week_data = get_weekly_completed_tasks(self.user_id)
        
        self.bar_set.remove(0, self.bar_set.count())
        self.bar_set.append(week_data)

    
class UpcomingDeadlinesCard(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(style())
        self.setObjectName('deadlinescard')

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(10)

        title = QLabel('Upcoming Deadlines')
        title.setObjectName('title_deadlinescard')

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.tasks_layout = QVBoxLayout(container)
        container.setStyleSheet('background-color: white')
        self.tasks_layout.setSpacing(8)

        scroll.setWidget(container)
        self.layout.addWidget(title)
        self.layout.addWidget(scroll)
    
    def load_data(self, tasks):
        self.setStyleSheet(style())

        for i in reversed(range(self.tasks_layout.count())):

            widget = self.tasks_layout.itemAt(i).widget()

            if widget:
                widget.deleteLater()
        
        for name, due_date, priority in tasks:
            task_label = QLabel(f'{name} | Due: {due_date} ⚠️ | {priority}')
            self.tasks_layout.addWidget(task_label)
            self.tasks_layout.addStretch()

class RecentActivityCard(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(style())
        self.setObjectName('activitycard')

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel('Recent Activity')
        title.setObjectName('title_activitycard')
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName('scroll')

        container = QWidget()
        container.setStyleSheet("background-color: white")
        self.activity_layout = QVBoxLayout(container)
        self.activity_layout.setSpacing(8)

        scroll.setWidget(container)
        layout.addWidget(scroll)
    
    def load_data(self, activities):
        for i in reversed(range(self.activity_layout.count())):
            widget = self.activity_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        for message, created_at in activities:
            label = QLabel(f"{message}\n{created_at}")
            self.activity_layout.addWidget(label)
        self.activity_layout.addStretch()

class category_dialog(QDialog):
    def __init__(self, user_id):
        super().__init__()

        self.setStyleSheet(style())

        self.user_id = user_id

        self.setFixedSize(200, 200)
        self.setWindowTitle('Create Category')
        self.setWindowIcon(QIcon('desktop_app/app/images/workspace_icon.png'))

        title = QLabel('Create Category')
        title.setObjectName('dialog_title')

        subtitle = QLabel('Insert Data')
        subtitle.setObjectName('dialog_subtitle')

        self.category_name = QLineEdit()
        self.category_name.setPlaceholderText('Category Name')
        self.category_name.setObjectName('dialog_createcategory')

        save_btn = QPushButton('Save')
        save_btn.setObjectName('dialog_btn')
        save_btn.clicked.connect(self.pressed_save)

        self.warning_text = QLabel('')

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.category_name)
        layout.addWidget(save_btn)
        layout.addWidget(self.warning_text)

    def pressed_save(self):
        if not all ([self.category_name.text()]):
            self.warning_text.setText('Category Name Cannot Be Blank')
            self.warning_text.setStyleSheet('color: #FD2E2E;')
            return
        success = create_category(self.category_name.text(), self.user_id)

        if success:
            self.warning_text.setText('Category Created')
            self.warning_text.setStyleSheet('color: #53FF4D')
            self.category_name.clear()
        else:
            self.warning_text.setText('Error Creating Category')
            self.warning_text.setStyleSheet('color: #FD2E2E')
    

class task_dialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)

        self.user_id = user_id

        self.setStyleSheet(style())

        self.setWindowTitle('Create Task')
        self.setFixedSize(300, 500)
        self.setWindowIcon(QIcon('desktop_app/app/images/workspace_icon.png'))

        title = QLabel('Create Task')
        title.setObjectName('dialog_title')

        subtitle = QLabel('Insert Data')
        subtitle.setObjectName('dialog_subtitle')

        self.category = QComboBox()
        self.category.setPlaceholderText('Category')

        categories = load_categories(self.user_id)

        for cat_id, name in categories:
            self.category.addItem(name, cat_id)

        self.task_name = QLineEdit()
        self.task_name.setPlaceholderText('Task Name')
        self.task_name.setObjectName('dialog_createcategory')

        self.task_description = QTextEdit()
        self.task_description.setPlaceholderText('Task Description')
        self.task_description.setObjectName('dialog_taskdescription')

        self.priority = QComboBox()
        self.priority.setPlaceholderText('Priority Level')
        self.priority.addItem('Low', 1)
        self.priority.addItem('Medium', 2)
        self.priority.addItem('High', 3)

        date_label = QLabel('Due Date 📅')

        self.due_date = QDateEdit()
        self.due_date.setCalendarPopup(True)
        self.due_date.setDate(QDate.currentDate())
        self.due_date.setDisplayFormat('dd/MM/yyyy')

        date_layout = QHBoxLayout()
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.due_date)

        save_btn = QPushButton('Save')
        save_btn.setObjectName('dialog_btn')
        save_btn.clicked.connect(self.save_task)

        self.warning_text = QLabel('')

        layout = QVBoxLayout(self)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(self.category)
        layout.addWidget(self.task_name)
        layout.addWidget(self.task_description)
        layout.addWidget(self.priority)
        layout.addLayout(date_layout)
        layout.addWidget(save_btn)
        layout.addWidget(self.warning_text)

    def save_task(self):
        category_id = self.category.currentData()
        priority = self.priority.currentData()
        due_date = self.due_date.date().toString('yyyy-MM-dd')

        name = self.task_name.text().strip()
        description = self.task_description.toPlainText().strip()

        if (
            category_id is None or
            priority is None or
            not name or
            not description
        ):
            self.warning_text.setText('Fill All Empty Fields')
            self.warning_text.setStyleSheet('color: #FD2E2E;')
            return
        
        success = create_task(self.task_name.text(), self.task_description.toPlainText(), priority, due_date, self.user_id, category_id)

        if success:
            self.warning_text.setText('Task Created')
            self.warning_text.setStyleSheet('color: #53FF4D')
            self.parent().refresh_metrics()
            self.accept()
        else:
            self.warning_text.setText('Error Creating Task')
            self.warning_text.setStyleSheet('color: #FD2E2E')


class Dashboard(QFrame):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        
        self.setStyleSheet(style())
        self.setObjectName('dashboard')

        title = QLabel('Dashboard')
        title.setObjectName('dashboard_title')

        category_btn = QPushButton('Add Category')
        category_btn.clicked.connect(self.category_screen)

        task_btn = QPushButton('Add Task')
        task_btn.clicked.connect(self.task_screen)

        top_buttons = [category_btn, task_btn]

        for btn in top_buttons:
            btn.setObjectName('top_btn')
            btn.setFixedSize(114, 34)
            shadow = QGraphicsDropShadowEffect(btn)
            shadow.setBlurRadius(15)
            shadow.setOffset(0, 2)
            shadow.setColor(QColor(0, 0, 0, 90))
            btn.setGraphicsEffect(shadow)

        top_layout = QHBoxLayout()
        top_layout.addWidget(title)
        top_layout.addWidget(category_btn)
        top_layout.addWidget(task_btn)

        total_tasks = count_tasks(user_id)
        completed_tasks = count_completed_status(user_id)
        pending_tasks = count_pending_tasks(user_id)
        overdue_tasks = count_overdue_tasks(user_id)

        self.total_card = MetricCard('Total Tasks 📋', str(total_tasks))
        self.completed_card = MetricCard('Completed Tasks ✅', str(completed_tasks))
        self.pending_card = MetricCard('Pending Tasks ⚠️', str(pending_tasks))
        self.overdue_card = MetricCard('Overdue Tasks ⏰', str(overdue_tasks))

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        cards_layout.addWidget(self.total_card)
        cards_layout.addWidget(self.completed_card)
        cards_layout.addWidget(self.pending_card)
        cards_layout.addWidget(self.overdue_card)

        categories_layout = QVBoxLayout()
        self.category_progress_card = CategoryProgressCard()
        categories_layout.addWidget(self.category_progress_card)

        self.chart_card = ChartCard(
            task_backend=get_weekly_completed_tasks,
            user_id=user_id
        )

        middle_layout = QHBoxLayout()
        middle_layout.addLayout(categories_layout)
        middle_layout.addLayout(self.chart_card.get_widget_with_categories())

        self.upcoming_card = UpcomingDeadlinesCard()
        self.recent_activity_card = RecentActivityCard()

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.upcoming_card)
        bottom_layout.addWidget(self.recent_activity_card)

        self.refresh_metrics()

        v_layout = QVBoxLayout(self)
        v_layout.addLayout(top_layout)
        v_layout.addLayout(cards_layout)
        v_layout.addLayout(middle_layout)
        v_layout.addLayout(bottom_layout)

    def category_screen(self):
        dialog = category_dialog(self.user_id)
        dialog.exec_()

    def task_screen(self):
        dialog = task_dialog(self.user_id, self)
        dialog.exec_()
    
    def refresh_metrics(self):
        total_tasks = count_tasks(self.user_id)
        completed_tasks = count_completed_status(self.user_id)
        pending_tasks = count_pending_tasks(self.user_id)
        overdue_tasks = count_overdue_tasks(self.user_id)

        self.total_card.update_value(str(total_tasks))
        self.completed_card.update_value(str(completed_tasks))
        self.pending_card.update_value(str(pending_tasks))
        self.overdue_card.update_value(str(overdue_tasks))

        self.load_category_progress()
        self.load_upcoming_deadlines()
        self.load_recent_activity()
        self.chart_card.refresh_weekly_chart()
    
    def load_category_progress(self):
        data = category_statistics(self.user_id)
        self.category_progress_card.load_data(data)
    
    def load_upcoming_deadlines(self):
        data = get_upcoming_deadlines(self.user_id)
        self.upcoming_card.load_data(data)
    
    def load_recent_activity(self):
        data = get_recent_activity(self.user_id)
        self.recent_activity_card.load_data(data)

#----------------CATEGORIES--------------------
class Categories(QFrame):
    def __init__(self, user_id, dashboard):
        super().__init__()
        self.dashboard = dashboard
        self.user_id = user_id
        self.setStyleSheet(style())

        title = QLabel('Categories')
        title.setObjectName('categories_title')

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        container = QWidget()
        self.categories_layout = QVBoxLayout(container)

        self.scroll.setWidget(container)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.scroll)
        self.load_category_list()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_category_list(self):
        self.clear_layout(self.categories_layout)
        categories = load_categories(self.user_id)

        for cat_id, name in categories:
            self.categories_layout.addWidget(
                self.create_category_card(cat_id, name)
            )

        self.categories_layout.addStretch()
    
    def create_category_card(self, cat_id, name):
        self.setStyleSheet(style())
        frame = QFrame()
        layout = QHBoxLayout(frame)
        label = QLabel(name)
        label.setObjectName('cat_name')

        view_btn = QPushButton('View Tasks')
        delete_btn = QPushButton('Delete')

        for i in view_btn, delete_btn:
            i.setObjectName('catbtn')
            shadow = QGraphicsDropShadowEffect(i)
            shadow.setBlurRadius(14)
            shadow.setOffset(2, 4)
            shadow.setColor(QColor(0, 0, 0, 60))
            i.setGraphicsEffect(shadow)

        view_btn.clicked.connect(lambda: self.open_tasks(cat_id, name))
        delete_btn.clicked.connect(lambda: self.delete_categories(cat_id, self.user_id))

        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(view_btn)
        layout.addWidget(delete_btn)

        return frame
    
    def delete_categories(self, cat_id, user_id):
        delete_category(cat_id, user_id)
        self.load_category_list()
        self.dashboard.refresh_metrics()
    
    def open_tasks(self, cat_id, name):
        self.clear_layout(self.categories_layout)
        self.current_category_name = name

        back_btn = QPushButton('Back')
        back_btn.clicked.connect(self.load_category_list)
        back_btn.setObjectName('back_cat')
        back_btn.setFixedWidth(140)

        title = QLabel(f'{name}')
        title.setObjectName('cat_tasks')

        self.categories_layout.addWidget(title)

        tasks = get_tasks_by_category(self.user_id, cat_id)

        for task in tasks:
            task_id, task_name, status, due_date, priority = task
            is_overdue = status == 'pending' and due_date.date() < date.today()

            self.categories_layout.addWidget(self.create_task_row(task_id, task_name, status, is_overdue, cat_id))
        self.categories_layout.addStretch()
        self.categories_layout.addWidget(back_btn)
    
    def create_task_row(self, task_id, name, status, is_overdue, cat_id):

        frame = QFrame()
        layout = QHBoxLayout(frame)
        label = QLabel(name)
        label.setObjectName('complete_label')

        if status == 'completed':
            label.setStyleSheet('color: blue')
        elif is_overdue:
            label.setStyleSheet('color: red;')

        complete_btn = QPushButton('✅')
        delete_btn = QPushButton('🗑️')

        for o in complete_btn, delete_btn:
            o.setObjectName('catbtn')

        complete_btn.clicked.connect(
        lambda: self.complete_task_list(task_id, cat_id)
    )

        delete_btn.clicked.connect(
            lambda: self.delete_task_list(task_id, cat_id)
        )

        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(complete_btn)
        layout.addWidget(delete_btn)

        return frame
            

    def complete_task_list(self, task_id, cat_id):
        complete_task(task_id, self.user_id, cat_id)
        self.open_tasks(cat_id, self.current_category_name)
        self.dashboard.refresh_metrics()
    
    def delete_task_list(self, task_id, cat_id):
        delete_task(task_id, self.user_id, cat_id)
        self.open_tasks(cat_id, self.current_category_name)
        self.dashboard.refresh_metrics()

#----------------STATISTICS--------------------
class Statistics(QFrame):
    def __init__(self, user_id):
        super().__init__()

        self.setStyleSheet(style())
        title = QLabel('Statistics')
        title.setObjectName('statistics_title')

        layout = QVBoxLayout(self)

        chart_card = ChartCard(
            task_backend=get_weekly_completed_tasks,
            user_id=user_id
        )

        layout.addWidget(title)
        layout.addLayout(chart_card.get_widget_with_categories())

#----------------ABOUT ME--------------------
class About_me(QDialog):
    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowIcon(QIcon('desktop_app/app/images/workspace_icon.png'))
        self.setStyleSheet(style())
        self.setWindowTitle('My Profile')

        self.setObjectName('about_me')
        self.setFixedSize(450, 500)

        title = QLabel('About Me')
        title.setObjectName('aboutme_title')

        name = QLabel('Full Name')
        fullname = QLabel(f"{self.user['firstname']} {self.user['lastname']}")

        username = QLabel('Username')
        username_data = QLabel(f'{self.user['username']}')

        email = QLabel('Email')
        email_data = QLabel(f'{self.user['email']}')

        total_tasks = count_tasks(user['id'])
        total_categories = count_categories(user['id'])

        tasks = QLabel('Total Tasks')
        tasks_number = QLabel(str(total_tasks))
        
        categories = QLabel('Total Categories')
        categories_number = QLabel(str(total_categories))

        for i in name, username, email, tasks, categories:
            i.setObjectName('aboutme_indicator')

        for i in fullname, username_data, email_data, tasks_number, categories_number:
            i.setObjectName('aboutme_data')

        name_layout = QHBoxLayout()
        name_layout.setSpacing(5)
        name_layout.addWidget(name, alignment=Qt.AlignCenter)
        name_layout.addWidget(fullname, alignment=Qt.AlignCenter)

        username_layout = QHBoxLayout()
        username_layout.setSpacing(5)
        username_layout.addWidget(username, alignment=Qt.AlignCenter)
        username_layout.addWidget(username_data, alignment=Qt.AlignCenter)

        email_layout = QHBoxLayout()
        email_layout.setSpacing(5)
        email_layout.addWidget(email, alignment=Qt.AlignCenter)
        email_layout.addWidget(email_data, alignment=Qt.AlignCenter)

        tasks_layout = QHBoxLayout()
        tasks_layout.setSpacing(5)
        tasks_layout.addWidget(tasks, alignment=Qt.AlignCenter)
        tasks_layout.addWidget(tasks_number, alignment=Qt.AlignCenter)

        categories_layout = QHBoxLayout()
        categories_layout.setSpacing(5)
        categories_layout.addWidget(categories, alignment=Qt.AlignCenter)
        categories_layout.addWidget(categories_number, alignment=Qt.AlignCenter)

        for i in name_layout, username_layout, email_layout, tasks_layout, categories_layout:
            i.setContentsMargins(80, 0, 80, 0)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.addWidget(title)
        layout.addLayout(name_layout)
        layout.addLayout(username_layout)
        layout.addLayout(email_layout)
        layout.addLayout(tasks_layout)
        layout.addLayout(categories_layout)

    
#----------------MAINWINDOW(Organizador Geral)--------------------
class MainWindow(QFrame):
    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setStyleSheet(style())
        
        self.setFixedSize(1200, 600)
        self.setWindowIcon(QIcon('desktop_app/app/images/workspace_icon.png'))
        self.setWindowTitle('WorkSpace')

        root = QVBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.SideBar = SideBar(self.user['firstname'], self.user)
        self.Dashboard = Dashboard(self.user['id'])
        self.Categories = Categories(self.user['id'], self.Dashboard)
        self.Statistics = Statistics(self.user['id'])

        self.stack = QStackedLayout()
        self.stack.addWidget(self.Dashboard)
        self.stack.addWidget(self.Categories)
        self.stack.addWidget(self.Statistics)

        self.SideBar.dashboard_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.SideBar.categories_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.SideBar.statistics_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.SideBar)
        horizontal_layout.addLayout(self.stack)

        root.addLayout(horizontal_layout)
        self.setLayout(root)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    app.setStyleSheet(style())

    window.show()
    sys.exit(app.exec())