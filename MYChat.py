scr = """
ScreenManager:
    #id = scm
    MainScreen:
    SecScreen: 
<MainScreen>
    name: 'main'
    MDScreen:
        md_bg_color: [0,0.5,0.8,0.4] #[47/255,39/255,107/255,1]
        MDCard:
            size_hint: None,None
            size: 320,400
            pos_hint: {'center_x':0.5,'center_y':0.5}
            elevation: 15
            padding: 20
            spacing: 30
            orientation: "vertical"
            MDLabel:
                text: "Login"
                font_style: 'Button'
                font_size: 20
                halign: "center"
                size_hint_y: None
                height: self.texture_size[1]
                padding_y: 15
            MDTextField:
                id: un
                hint_text: "Enter Username"
                icon_right: "account"
                helper_text: "Keep it short"
                helper_text_mode: "persistent"
                pos_hint: {"center_x": 0.5,"center_y": 0.2}
                size_hint_x: None
                width: "230px"
                font_size: 20
                multiline: False
                required: True
                color_active: [1,1,1,1]
            MDTextField:
                id: pwd
                hint_text: "Enter Password"
                icon_right: "eye-off"
                helper_text: "Its Optional to enter password"
                helper_text_mode: "on_focus"
                pos_hint: {"center_x": 0.5,"center_y": 0.2}
                size_hint_x: None
                width: "230px"
                font_size: 20
                multiline: False
                required: False
                color_active: [1,1,1,1]
                password: True
                required: True

            MDRoundFlatButton:
                id: login1
                text: "Login"
                pos_hint: {"center_x": 0.5}
                font_size: 15
                on_press: root.manager.current = 'sec'
            Widget:
                size_hint_y: None
                height: 15

<SecScreen>
    name: 'sec'
    #id: 's2'                    
    MDScreen:
        
        BoxLayout: 
            orientation: "vertical"
            ScrollView:
                id: sv
                padding: 20
                MDList:
                    label: 'The Messages'
                    #icon: 'face'
                    halign: 'right'
                    selected_chip_color: .21176470535294, .098039627451, 1, 1
                

            BoxLayout: 
                orientation: "vertical"
                padding: 10  
                MDTextField:
                    id: 'msg'
                    hint_text: "Type Message"
                    mode: "rectangle"
                    helper_text: "Type your message"
                    helper_text_mode: "on_focus"
                    pos_hint: {"center_x": 0.5,"center_y": 0.1}
                    size_hint_x: None
                    width: "250px" 
                    font_size: 15             
                    multiline: True
                    required: False
                    padding_y: "20dp"

                MDFillRoundFlatButton: 
                    #id: sendb
                    text: 'Send' 
                    font_size: 15 
                    md_bg_color: [0,0.5,0.8,0.5]
                    #text_color = [0,0,0,1]
                    width: 200
                    pos_hint: {'center_x': 0.5,'center_y':0.1}
                    on_press: root.manager.current = app.dj()      


"""