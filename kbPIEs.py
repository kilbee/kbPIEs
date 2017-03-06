bl_info = {
    "name": "kbPIEs",
    "author": "kilbeeu",
    "version": (0, 2),
    "blender": (2, 78, 0),
    "description": "Adds a PIE Menu for switching Screen Layouts",
    "warning": "",
    "wiki_url": "http://github.com/kilbee/kbPIEs",
    "tracker_url":"https://gitreports.com/issue/kilbee/kbPIEs",
    "category": "Pie Menu",
}


import bpy
import rna_keymap_ui


def avail_screens(self,context):
    screens = [     ('Maximize Area', 'Maximize Area', 'Maximizes current area'),
                    ('User Preferences', 'User Preferences', 'User Preferences')
                ] # (identifier, name, description) optionally: (.., icon name, unique number)
    
    for i, screen in enumerate(bpy.data.screens):
        screens.append((screen.name, screen.name, screen.name))
    return screens


def add_hotkey():
    user_preferences = bpy.context.user_preferences
    addon_prefs = user_preferences.addons[__name__].preferences
    
    kc = bpy.context.window_manager.keyconfigs.user
    km = kc.keymaps['Screen']
    kmi = km.keymap_items.new("wm.call_menu_pie", "NONE", "PRESS")
    kmi.properties.name = "KbPiesSwitchLayout"
    kmi.active = True


def get_addon_preferences():
    addon_preferences = bpy.context.user_preferences.addons[__name__].preferences
    return addon_preferences




class KbPiesAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__


    kb_pie_screens_top_left     = bpy.props.StringProperty( name="Top Left",     default="Maximize Area" )
    kb_pie_screens_top          = bpy.props.StringProperty( name="Top",          default="Maximize Area" )
    kb_pie_screens_top_right    = bpy.props.StringProperty( name="Top Right",    default="Maximize Area" )

    kb_pie_screens_left         = bpy.props.StringProperty( name="Left",         default="Maximize Area" )
    kb_pie_screens_right        = bpy.props.StringProperty( name="Right",        default="Maximize Area" )

    kb_pie_screens_bottom_left  = bpy.props.StringProperty( name="Bottom Left",  default="Maximize Area" )
    kb_pie_screens_bottom       = bpy.props.StringProperty( name="Bottom",       default="Maximize Area" )
    kb_pie_screens_bottom_right = bpy.props.StringProperty( name="Bottom Right", default="Maximize Area" )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        #split = row.split(percentage=0.33)
        split = row.split()
        col = split.column()
        col.operator_menu_enum('kbpies.select_screen', 'top_left', text='Top Left ({})'.format(self.kb_pie_screens_top_left))
        col.operator_menu_enum('kbpies.select_screen', 'left', text='Left ({})'.format(self.kb_pie_screens_left))
        col.operator_menu_enum('kbpies.select_screen', 'bottom_left', text='Bottom left ({})'.format(self.kb_pie_screens_bottom_left))
        
        
        #split = split.split(percentage=0.66)
        split = row.split()
        col = split.column()
        col.operator_menu_enum('kbpies.select_screen', 'top', text='Top ({})'.format(self.kb_pie_screens_top))
        col.separator()
        col.separator()
        col.separator()
        col.operator_menu_enum('kbpies.select_screen', 'bottom', text='Bottom ({})'.format(self.kb_pie_screens_bottom))
        
        split = row.split()
        col = split.column()
        col.operator_menu_enum('kbpies.select_screen', 'top_right', text='Top Right ({})'.format(self.kb_pie_screens_top_right))
        col.operator_menu_enum('kbpies.select_screen', 'right', text='Right ({})'.format(self.kb_pie_screens_right))
        col.operator_menu_enum('kbpies.select_screen', 'bottom_right', text='Bottom Right ({})'.format(self.kb_pie_screens_bottom_right))
        
        

        layout.separator()
        # hotkey section
        box = layout.box()
        col = box.column()        
        col.label('Setup Hotkey')
        col.separator()
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps['Screen']
        if 'wm.call_menu_pie' in km.keymap_items.keys():
            kmi = km.keymap_items["wm.call_menu_pie"]
            #km = km.active()
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
            col.separator()
            col.label(text="Hotkey also listed in User Preferences -> Input -> Screen -> Screen (Global)")
        else:
            col.label("No hotkey entry found")
            col.operator(KbPiesAddHotkey.bl_idname, text = "Add hotkey entry", icon = 'ZOOMIN')
        #layout.separator()
        #layout.operator("wm.url_open", text="homepage & more info").url = "http://kilbeeu.wordpress.com"


    def execute(self,context):
        self.bl_label = self.select_screen
        print(self.select_screen)
        return {'FINISHED'}

        
        


class KbPiesSelectScreen(bpy.types.Operator):
    ''' set screen layout to corresponding pie position '''
    bl_idname = "kbpies.select_screen"
    bl_label = "Select screen"
    num =  bpy.props.IntProperty()

    top_left    = bpy.props.EnumProperty( name = "Top Left",    items = avail_screens)
    left        = bpy.props.EnumProperty( name = "Left",        items = avail_screens)
    bottom_left = bpy.props.EnumProperty( name = "Bottom Left", items = avail_screens)

    top         = bpy.props.EnumProperty( name = "Top",         items = avail_screens)
    bottom      = bpy.props.EnumProperty( name = "Bottom",      items = avail_screens)

    top_right   = bpy.props.EnumProperty( name = "Top Right",   items = avail_screens)
    right       = bpy.props.EnumProperty( name = "Right",       items = avail_screens)
    bottom_right= bpy.props.EnumProperty( name = "Bottom Right",items = avail_screens)

    
    def execute(self,context):
        addon_preferences = get_addon_preferences()

        addon_preferences.kb_pie_screens_top_left = self.top_left
        addon_preferences.kb_pie_screens_left = self.left
        addon_preferences.kb_pie_screens_bottom_left = self.bottom_left

        addon_preferences.kb_pie_screens_top = self.top
        addon_preferences.kb_pie_screens_bottom = self.bottom

        addon_preferences.kb_pie_screens_top_right = self.top_right
        addon_preferences.kb_pie_screens_right = self.right
        addon_preferences.kb_pie_screens_bottom_right = self.bottom_right

        return {'FINISHED'}
        

               
        

class KbPiesSwitchLayout(bpy.types.Menu):
    bl_label = "Screen Layout"   # label is displayed at the center of the pie menu.   

    def draw(self, context):
        addon_preferences = get_addon_preferences()
        bottom_left  = addon_preferences.kb_pie_screens_bottom_left
        bottom       = addon_preferences.kb_pie_screens_bottom
        bottom_right = addon_preferences.kb_pie_screens_bottom_right
        left         = addon_preferences.kb_pie_screens_left
        right        = addon_preferences.kb_pie_screens_right
        top_left     = addon_preferences.kb_pie_screens_top_left
        top          = addon_preferences.kb_pie_screens_top
        top_right    = addon_preferences.kb_pie_screens_top_right
        
        pie = self.layout.menu_pie()
        # Basic 4 direction PIE
        pie.operator("screen.set_layout", left).layoutName = left
        pie.operator("screen.set_layout", right).layoutName = right
        pie.operator("screen.set_layout", bottom).layoutName = bottom
        pie.operator("screen.set_layout", top).layoutName = top

        # Additional 4 directions PIE
        pie.operator("screen.set_layout", top_left).layoutName = top_left
        pie.operator("screen.set_layout", top_right).layoutName = top_right
        pie.operator("screen.set_layout", bottom_left).layoutName = bottom_left
        pie.operator("screen.set_layout", bottom_right).layoutName = bottom_right





class KbPiesSetScreenLayout(bpy.types.Operator):
    ''' change screen layout '''
    bl_idname="screen.set_layout"
    bl_label="Switch to Screen Layout"
    layoutName=bpy.props.StringProperty()   
    
    def execute(self,context):
        if self.layoutName == "Maximize Area":  # if just want to MAXIMIZE area then do so:
            bpy.ops.screen.screen_full_area()
            return{'FINISHED'}
        elif self.layoutName == "User Preferences":
            bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
            #bpy.context.user_preferences.active_section = 'ADDONS'
            return{'FINISHED'}
        else:
            try:
                if bpy.context.window.screen.show_fullscreen:
                    bpy.ops.screen.back_to_previous() # if area is maximized back to previous layout before switching it (avoids some crashes)
                bpy.context.window.screen=bpy.data.screens[self.layoutName] # try to switch layout
            except:
                # except layout doesn't exists
                self.report({'INFO'}, 'Screen layout [{}] doesn\'t exist! Create it or pick another in addon settings.'.format(self.layoutName))
        return{'FINISHED'}
 





class KbPiesAddHotkey(bpy.types.Operator):
    ''' add hotkey entry '''
    bl_idname = "kbpies.add_hotkey"
    bl_label = "Addon Preferences Example"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        add_hotkey()

        self.report({'INFO'}, "Hotkey added in User Preferences -> Input -> Screen -> Screen (Global)")
        return {'FINISHED'}









def register():
    bpy.utils.register_class(KbPiesSelectScreen)
    bpy.utils.register_class(KbPiesSwitchLayout)
    bpy.utils.register_class(KbPiesSetScreenLayout)    
    bpy.utils.register_class(KbPiesAddonPreferences)
    bpy.utils.register_class(KbPiesAddHotkey)
    

    # hotkey setup
    # http://blender.stackexchange.com/a/1498/1610
    kc = bpy.context.window_manager.keyconfigs.user
    if 'Screen' in kc.keymaps.keys():
        #bpy.ops.kbpies.add_hotkey('EXEC_DEFAULT') 
        add_hotkey()





def unregister():
    bpy.utils.unregister_class(KbPiesSelectScreen)
    bpy.utils.unregister_class(KbPiesSwitchLayout)
    bpy.utils.unregister_class(KbPiesSetScreenLayout)
    bpy.utils.unregister_class(KbPiesAddonPreferences)
    bpy.utils.unregister_class(KbPiesAddHotkey)

    # hotkey cleanup
    # kc = bpy.context.window_manager.keyconfigs.user
    # km = kc.keymaps['Screen']
    # if 'wm.call_menu_pie' in km.keymap_items.keys():
    #     kmi = km.keymap_items["wm.call_menu_pie"]
    #     km.keymap_items.remove(kmi)

