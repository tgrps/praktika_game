

import arcade
import os
import random
import shelve



SCREEN_WIDTH = 271
SCREEN_HEIGHT = 651
SCREEN_TITLE = "Mimi ship"
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 3
VIEWPORT_MARGIN = 400
BULLET_SPEED = 6
IMAGE_WIDTH = 271
IMAGE_HEIGHT = 651
SCROLL_SPEED = 3




    
class MainMenu(arcade.View):
    

    def on_show_view(self):        
        arcade.set_background_color(arcade.color.SAE)

    def on_draw(self):
        
        self.clear()
        arcade.draw_text(
            "START",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        self.window.show_view(game_view)



class AnimatedWalkingSprite(arcade.AnimatedWalkingSprite):
    def __init__(self) -> None:
        super().__init__(CHARACTER_SCALING)
        self.stand_right_textures = None
        self.stand_right_textures = None
        self.walk_left_textures = None
        self.walk_right_textures = None
        



class MyGame(arcade.View):

    def __init__(self):
        
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        
        self.wall_list = None 
        self.player_list = None
        self.bullet_list = None
        self.background = None
        self.enemy_list = None
        self.coin_list = None        
        self.player_sprite = None
        self.physics_engine = None
        self.score = 0
        self.view_bottom = 0
        self.view_left = 0
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):

        self.enemy_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        self.background_sprite = arcade.Sprite("assets/bg.png")
        self.background_sprite.center_y = IMAGE_HEIGHT // 2
        self.background_sprite.center_x = SCREEN_WIDTH // 2
        self.background_sprite.change_y = -SCROLL_SPEED
        self.background_list.append(self.background_sprite)

        self.background_sprite2 = arcade.Sprite("assets/bg2.png")
        self.background_sprite2.center_y = SCREEN_HEIGHT + IMAGE_HEIGHT // 2
        self.background_sprite2.center_x = SCREEN_WIDTH // 2
        self.background_sprite2.change_y = -SCROLL_SPEED
        self.background_list.append(self.background_sprite2)
        

        self.score = 0
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.AnimatedWalkingSprite()

        self.player_sprite.stand_right_textures= []
        self.player_sprite.stand_right_textures.append(arcade.load_texture("assets/ship4.png"))

        self.player_sprite.stand_left_textures= []
        self.player_sprite.stand_left_textures.append(arcade.load_texture("assets/ship.png"))

        self.player_sprite.walk_right_textures= []
        self.player_sprite.walk_right_textures.append(arcade.load_texture("assets/ship.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("assets/ship2.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("assets/ship3.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("assets/ship4.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("assets/ship5.png"))
      

        self.player_sprite.walk_left_textures= []
        self.player_sprite.walk_left_textures.append(arcade.load_texture("assets/ship2.png"))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("assets/ship3.png"))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("assets/ship3.png"))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("assets/ship5.png"))

        self.player_sprite.walk_left_textures.append(arcade.load_texture("assets/ship.png"))
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite.center_x = 135

        self.player_sprite.center_y = 128

        self.player_list.append(self.player_sprite)

        self.view_left = 0
        self.view_bottom = 0



        coordinate_list = [[135, 1]]
        coordinate_list_2 = [[1, 128],[270,128]]

        self.bullet_list = arcade.SpriteList()

        for coordinate in coordinate_list:

            wall = arcade.Sprite(
                "assets/wall.png", CHARACTER_SCALING
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
            self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )
            self.wall_list.append(wall)

        for coordinate in coordinate_list_2:
            wall = arcade.Sprite(
                "assets/wall2.png", CHARACTER_SCALING
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
            self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )
            self.wall_list.append(wall)


    def on_show_view(self):
        self.setup()


    def on_key_press(self, key, modifiers):
                
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED


    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):

        bullet = arcade.Sprite("assets/bullet.png", CHARACTER_SCALING)
        bullet.center_x=self.player_sprite.center_x
        bullet.center_y=self.player_sprite.center_y +30
        bullet.change_y=BULLET_SPEED
        bullet.angle = 90
        self.bullet_list.append(bullet)
        
    def on_update(self, delta_time):

        self.bullet_list.update()
        for bullet in self.bullet_list:


            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list) 
            hit_list2 = arcade.check_for_collision_with_list(bullet, self.coin_list) 

            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            if len(hit_list2) > 0:
                bullet.remove_from_sprite_lists()

            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 50
            for coin in hit_list2:
                coin.remove_from_sprite_lists()
                self.score += 100

            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()


        for enemy in self.enemy_list:
            
            hit_list3 = arcade.check_for_collision_with_list(enemy, self.wall_list)
            
            if len(hit_list3)>0:
                
                d = shelve.open('score.txt')  
                d.close()
                view = GameOverView()
                self.window.show_view(view)
            
            

        self.player_list.update_animation()

        self.physics_engine.update()
        
       
        if self.background_sprite.top == IMAGE_HEIGHT:
            self.background_sprite2.center_y = SCREEN_HEIGHT + IMAGE_HEIGHT //2
            
                   
        if self.background_sprite2.top == IMAGE_HEIGHT:
            self.background_sprite.center_y = SCREEN_HEIGHT + IMAGE_HEIGHT //2

        self.background_list.update()
        
        if random.random() < 0.01:
            enemy = arcade.Sprite ("assets/meteorr.png",TILE_SCALING)
            enemy.bottom = 650
            enemy.center_x = random.randint(50, 200)
            self.enemy_list.append(enemy)

        for enemy in self.enemy_list:
            enemy.center_y -= 5

        if random.random() < 0.01:
            coin = arcade.Sprite ("assets/coin.png",CHARACTER_SCALING)
            coin.bottom = 650
            coin.center_x = random.randint(50, 200)
            self.coin_list.append(coin)

        for coin in self.coin_list:
            coin.center_y -= 5
            
    def on_draw(self):
        
        self.background_list.draw()       
        self.bullet_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        
        score_text = f"Score: {self.score}"        
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

class GameOverView(arcade.View):


    def __init__(self):

        super().__init__()
        arcade.set_background_color(arcade.color.SAE)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "GAME OVER - Click to play",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )
        d = shelve.open('score.txt')
        score = d['score']  
        d.close()
        arcade.draw_text(
             f"Score: {score}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 3,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )
   
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)

def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MainMenu()
    window.show_view(start_view)
    arcade.run()
   
    
if __name__ == "__main__":
    main()