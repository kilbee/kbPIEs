bl_info = {
    "name": "kbPIEs",
    "author": "kilbeeu",
    "version": (0, 1),
    "blender": (2, 74, 1),
    "description": "Adds a PIE Menu for switching Screen Layouts",
    "warning": "",
    "wiki_url": "http://kilbeeu.wordpress.com",
    "category": "User Interface",
}


import bpy
from bpy.types import Menu


class kbPIE_addon_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    kbPIEoptionNum4 = bpy.props.StringProperty(
            name="NumPad 4",
            default="Default",
            )
    kbPIEoptionNum6 = bpy.props.StringProperty(
            name="NumPad 6",
            default="UV Editing",
            )
    kbPIEoptionNum2 = bpy.props.StringProperty(
            name="NumPad 2",
            default="Animation",
            )
    kbPIEoptionNum8 = bpy.props.StringProperty(
            name="NumPad 8",
            default="3D View Full",
            )
    kbPIEoptionNum7 = bpy.props.StringProperty(
            name="NumPad 7",
            default="Compositing",
            )
    kbPIEoptionNum9 = bpy.props.StringProperty(
            name="NumPad 9",
            default="Motion Tracking",
            )
    kbPIEoptionNum1 = bpy.props.StringProperty(
            name="NumPad 1",
            default="Video Editing",
            )
    kbPIEoptionNum3 = bpy.props.StringProperty(
            name="NumPad 3",
            default="Maximize Area",
            )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        layout.label(text="Fill options with EXISTING layout names.")
        layout.label(text="To use option [Maximize Area] use this EXACT string [Maximize Area] without brackets.")
        layout.separator()
        layout.label(text="Hotkey Setup in User Preferences -> Input -> Screen -> Screen (Global)")
        layout.label(text="Add New -> Identifier: [wm.call_menu_pie], name: [kbPIE_switch_layout]")
            
        
        row = layout.row()
        layout.separator()
        layout.label(text="* Basic Cross options:")
        layout.prop(self, "kbPIEoptionNum4")
        layout.prop(self, "kbPIEoptionNum6")
        layout.prop(self, "kbPIEoptionNum2")
        layout.prop(self, "kbPIEoptionNum8")
        
        layout.separator()
        layout.label(text="* Sidelong Cross Options:")
        layout.prop(self, "kbPIEoptionNum7")
        layout.prop(self, "kbPIEoptionNum9")
        layout.prop(self, "kbPIEoptionNum1")
        layout.prop(self, "kbPIEoptionNum3")
        
        layout.separator()
        layout.operator("wm.url_open", text="homepage & more info").url = "http://kilbeeu.wordpress.com"




        

                
        

class kbPIE_switch_layout(Menu):
    bl_label = "Screen Layout"   # label is displayed at the center of the pie menu.   

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        executeOperator = "screen.set_layout"        
        
        # Define NUM options
        addon_preferences = get_addon_preferences()
        num1 = addon_preferences.kbPIEoptionNum1
        num2 = addon_preferences.kbPIEoptionNum2
        num3 = addon_preferences.kbPIEoptionNum3
        num4 = addon_preferences.kbPIEoptionNum4
        num6 = addon_preferences.kbPIEoptionNum6
        num7 = addon_preferences.kbPIEoptionNum7
        num8 = addon_preferences.kbPIEoptionNum8
        num9 = addon_preferences.kbPIEoptionNum9
        
        # Basic 4 direction PIE
        pie.operator(executeOperator, num4).layoutName = num4
        pie.operator(executeOperator, num6).layoutName = num6
        pie.operator(executeOperator, num2).layoutName = num2
        pie.operator(executeOperator, num8).layoutName = num8

        # Additional 4 directions PIE
        pie.operator(executeOperator, num7).layoutName = num7
        pie.operator(executeOperator, num9).layoutName = num9
        pie.operator(executeOperator, num1).layoutName = num1
        pie.operator(executeOperator, num3).layoutName = num3

        
        
        

class SetScreenLayout(bpy.types.Operator):
    bl_idname="screen.set_layout"
    bl_label="Switch to Screen Layout"
    layoutName=bpy.props.StringProperty()   
    
    def execute(self,context):
        if self.layoutName == "Maximize Area":  # if just want to MAXIMIZE area then do so:
            bpy.ops.screen.screen_full_area()
            return{'FINISHED'}
        else:
            try:
                if bpy.context.window.screen.show_fullscreen:               # if area is maximized back to previous layout before switching it (avoids some crashes):
                    bpy.ops.screen.back_to_previous()
                bpy.context.window.screen=bpy.data.screens[self.layoutName] # try to switch layout
            except:
                self.report({'INFO'}, 'Screen layout [%s] doesn\'t exist! Create it to use with kbPIE or pick another in addon settings.' % self.layoutName)  # except layout doesn't exists
        return{'FINISHED'}
 




def get_addon_preferences():
    addon_preferences = bpy.context.user_preferences.addons[__name__].preferences
    return addon_preferences


def register():
    bpy.utils.register_class(kbPIE_switch_layout)
    bpy.utils.register_class(SetScreenLayout)    
    bpy.utils.register_class(kbPIE_addon_preferences)

    # hotkey setup
    #km =  bpy.context.window_manager.keyconfigs.addon.keymaps.new(name="Screen (Global)")
    #kmi = km.keymap_items.new("wm.call_menu_pie", "F", "PRESS")
    #kmi.properties.name="kbPIE_switch_layout"


def unregister():
    bpy.utils.unregister_class(kbPIE_switch_layout)
    bpy.utils.unregister_class(SetScreenLayout)
    bpy.utils.unregister_class(kbPIE_addon_preferences)


# needed only for testing when run directly from text block as script:
#if __name__ == "__main__":
    #register()

    #bpy.ops.wm.call_menu_pie(name= "kbPIE_switch_layout")
