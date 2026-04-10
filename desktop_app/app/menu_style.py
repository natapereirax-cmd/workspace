#ESTILIZAÇÃO DA TELA DE MENU

def style():
    return """

    QPushButton#buttons {
        background-color: transparent;
        color: white;
        font-family: Bebas Neue;
        padding: 0px;
        font-size: 20px;
        border: none;
    }

    QPushButton:hover#buttons {
        background-color: #2c2e32;
        font-size: 25px;
    }

    QPushButton:checked#buttons {
        background-color: #2c2e32;
        border-left: 4px solid #4DA3FF;
    }
    
    QLabel#wlc {
        color: white;
        font-family: Caviar Dreams;
        font-size: 20px;
        font-weight: bold;
    }
    #dashboard {
        background-color: #e1e1e1;
    }

    QLabel#dashboard_title {
        font-size: 30px;
        font-family: Bebas Neue;
        color: #161719;
    }

    QPushButton#top_btn {
        background-color: white;
        border: 1px solid #222227;
        color: #222227;
        font-family: Caviar Dreams;
        border-radius: 8px;
        padding: 5px 12px;
        height: 36px;
        font-size: 12px;
    }

    QPushButton:hover#top_btn {
        background-color: #dddddd;
    }

    #metriccard {
        background-color: white;
    }
    
    #v_bar {
        background-color: #161719;
        border-top-left-radius: 12px;
        border-bottom-left-radius: 12px;
    }

    QLabel#metric_title {
        color: #111827;
        font-family: Bebas;
        font-size: 18px;
    }

    QLabel#metric_value {
        color: #393939;
        font-family: Caviar Dreams;
        font-size: 15px;
        font-weight: 550;
    }

    #CategoryProgressCard {
        background-color: white;
    }

    #CategoryProgressCard_title {
        color: #161719;
        font-family: Bebas;
        font-size: 18px;
    }

    QScrollBar:vertical {
        background: transparent;
        width: 10px;
        margin: 0px;
        }

    QScrollBar::handle:vertical {
        background: #161719;
        border-radius: 5px;
        min-height: 40px;
        }

    QScrollBar::handle:vertical:hover {
        background: #393939;
        }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0px;
        }

    QProgressBar {
            border: 1px solid #d1d5db;
            border-radius: 10px;
            background-color: #f3f4f6;
            text-align: center;
            font-weight: bold;
            height: 18px;
        }

    QProgressBar::chunk {
            border-radius: 10px;
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #4DA3FF,
                stop:1 #2563EB
            );
        }

    #category_stats {
        color: black;
        font-family: Caviar Dreams;
        font-size: 15px;
    }

    QFrame#ChartCard {
        background-color: #FFFFFF;
        border: none;
    }

    QFrame#deadlinescard {
        background-color: white;
    }

    QFrame#activitycard {
        background-color: white;
    }

    QLabel#title_activitycard {
        color: #161719;
        font-family: Bebas;
        font-size: 18px;
    }

    QLabel#title_deadlinescard {
        color: #161719;
        font-family: Bebas;
        font-size: 18px;
    }

    QLabel#dialog_title {
        font-size: 18px;
        font-family: Bebas Neue;
        color: #161719;
    }
 
    QLabel#dialog_subtitle {
        font-size: 14px;
        font-family: Caviar Dreams;
        color: #161719;
    }

    QLabel#dialog_createcategory {
        color: #5a5a5a;
    }
    
    QLineEdit#dialog_createcategory {
        background-color: #e6e9ee;
        color: #1e1e1e;
        border: 1px solid #b0b6bf;
        border-radius: 6px;
        padding: 8px;
    }

    QLineEdit:focus#dialog_createcategory {
    border: 1px solid #3a86ff;
    background-color: #edf0f5;
    }

    QPushButton#dialog_btn {
        background-color: transparent;
        color: #161719;
        font-family: Bebas Neue;
        padding: 0px;
        font-size: 30px;
        border: none;
    }

    QPushButton:hover#dialog_btn {
        font-size: 40px;
    }

    QLabel#dialog_taskdescription {
        color: #5a5a5a;
    }
        
    QTextEdit#dialog_taskdescription {
        background-color: #e6e9ee;
        color: #1e1e1e;
        border: 1px solid #b0b6bf;
        border-radius: 6px;
        padding: 8px;
        }
        QLineEdit:focus {
        border: 1px solid #3a86ff;
        background-color: #edf0f5;
        }

    #title_deadlinescard {
        color: #161719;
        font-family: Bebas;
        font-size: 18px;
    }

    #categories_title {
        font-size: 30px;
        font-family: Bebas Neue;
        color: #161719;
    }

    QLabel#statistics_title {
        font-size: 30px;
        font-family: Bebas Neue;
        color: #161719;
    }

    #about_me {
    background-color: #161719;
    }

    #aboutme_title {
        font-size: 40px;
        font-family: Bebas Neue;
        color: #ffffff;
    }

    #aboutme_indicator {
        font-size: 20px;
        font-family: Bebas Neue;
        color: #ffffff;
    }

    #aboutme_data {
        color: #ffffff;
        font-family: Caviar Dreams;
        font-size: 20px;
    }

    #catbtn {
        background-color: #161719;
        color: #ffffff;
        font-family: Bebas Neue;
        font-size: 15px;
    }
    QPushButton:hover#catbtn {
        font-size: 20px;
    }

    #cat_name {
        font-size: 20px;
        font-family: Caviar Dreams;
        color: #161719;
        font-weight: 600;
    }

    #cat_tasks {
        color: #161719;
        font-family: Bebas Neue;
        font-size: 25px;
    }

    #back_cat {
        background-color: #161719;
        color: #ffffff;
        font-family: Bebas Neue;
        font-size: 25px;
    }
    QPushButton:hover#back_cat {
        font-size: 30px;
    }

    #complete_label {
        font-size: 20px;
        font-family: Caviar Dreams;
        color: #161719;
        font-weight: 600;
    }
    

    """