from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def login(request):
    return render(request, 'login/login.html')

def process_login(request):
    if request.method == 'POST':
        errors = Player.objects.login_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        request.session['id'] = Player.objects.get(email = request.POST['email']).id
        request.session['username'] = Player.objects.get(email = request.POST['email']).username  
        if Player.objects.get(email = request.POST['email']).role == -1:
            return redirect('/register/pick_class')

        request.session['logged_in'] = True
        return redirect('/main')
    else:
        return redirect('/')

def register(request):
    return render(request, 'login/register.html')

def process_reg(request):
    if request.method == 'POST':
        errors = Player.objects.reg_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        
        player = Player(username = request.POST['username'], email = request.POST['email'], pass_hs= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()), level = 1, exp = 0, role = -1)
        player.save()
        request.session['id'] = player.id
        request.session['username'] = player.username
        return redirect('/register/pick_class')
    else:
        return redirect('/')

def pick_class(request):
    return render(request, 'login/pick_class.html')

def process_pick(request):
    if request.method == 'POST':
        player = Player.objects.get(id = request.session['id'])
        if request.POST['role'] == 'knight':
            player.role = 1
        elif request.POST['role'] == 'rogue':
            player.role = 2
        elif request.POST['role'] == 'mage':
            player.role = 3
        elif request.POST['role'] == 'ranger':
            player.role = 4
        elif request.POST['role'] == 'beserker':
            player.role = 5
        player.save()

        request.session['logged_in'] = True
        return redirect('/main')
    else:
        return redirect('/')

def main(request):
    role_id = Player.objects.get(id = request.session['id']).role
    level = Player.objects.get(id = request.session['id']).level - 1
    if role_id == 1:
        role = "Knight"
        hp = 50 + 5 * level
        atk = 4 + 2 * level
        defe = 10 + 4 * level
        s1_name = "Shield Wall"
        s1_desc = "Reduce damage taken from the enemy for a few turns. CD: 4"
        s2_name = "War Cry"
        s2_desc = "Attracts the enemy's attention and forces him/her to use only basic attack for a few turns. CD: 6"
        s3_name = "Crippling Blows"
        s3_desc = "Your normal attacks cripple the enemy, reducing their damage and stacks up to 5 times. CD: 6"
        s4_name = "Revenge"
        s4_desc = "Deal equal damange taken from an enemy back at the enemy for the next turn. CD: 3"

    elif role_id == 2:
        role = "Rogue"
        hp = 30 + 3 * level
        atk = 10 + 4 * level
        defe = 5 + 3 * level
        s1_name = "Poisoned knife"
        s1_desc = "Hurls a poisoned knife at the target. Deals damage over a few turns.. CD: 5"
        s2_name = "Paralytic Knife"
        s2_desc = "Throw a knife coated in a toxin that renders its victim helpless for a few turns. CD: 4"
        s3_name = "Expose Weakness"
        s3_desc = "If the enemy has an effect, youe next attack deals massive damage. CD: 7"
        s4_name = "Shadowstep"
        s4_desc = "Greatly increases dexterity and greatly increases damage of your next attack. CD: 5 "

    elif role_id == 3:
        role = "Mage"
        hp = 30 + 3 * level
        atk = 10 + 4 * level
        defe = 3 + 2 * level
        s1_name = "Fireball"
        s1_desc = "Launches a fireball at your enemy and burn them for a few turns. CD: 4"
        s2_name = "Blizzard"
        s2_desc = "Lowers the enemy attack and freezes the enemy for a few turns. CD: 4"
        s3_name = "Mage Shield"
        s3_desc = "Recovers some lost hp in the form of shield. CD: 4"
        s4_name = "Teleport"
        s4_desc = "Greatly increases evasiveness for the next few turns. CD: 8"

    elif role_id == 4:
        role = "Ranger"
        hp = 30 + 3 * level
        atk = 7 + 5 * level
        defe = 4 + 2 * level
        s1_name = "Aimed Shot"
        s1_desc = "A precisely aimed shot which deals more damage the less heatlh the enemy has. CD: 3"
        s2_name = "Vile Bolt"
        s2_desc = "A poisoned arrow which deals containuous damage and leaves the victim with less defense. CD: 5"
        s3_name = "Secret Trap"
        s3_desc = "A trap that lowers the enemy defense and lasts for 2 turns. Triggers whenever the enemy uses active skills. CD: 6"
        s4_name = "Apollo Strike"
        s4_desc = "A burtal shot that leaves the enemy unconscious for 2 turns. Only works if the enemy has less health than you. CD: 7"

    elif role_id == 5:
        role = "Beserker"
        hp = 40 + 4 * level
        atk = 7 + 3 * level
        defe = 6 + 3 * level
        s1_name = "Enrage"
        s1_desc = "Increasing damage dealt AND taken for a few turns. CD: 5"
        s2_name = "Death Wish"
        s2_desc = "Take away a portion of youe health and deal massive damage to the enemy. CD: 3"
        s3_name = "Bloodthirsty"
        s3_desc = "Your next few attacks recovers some of your HP based on your damage. CD: 6"
        s4_name = "Adrenaline Rush"
        s4_desc = "Your attack is increased for the next few turns and also apply a bleeding effect. CD: 5"

    recent_players = []
    for game in Player.objects.get(id = request.session['id']).games.order_by('-id')[:3]:
        for player in game.players.all():
            if player.id != request.session['id']:
                recent_players.append(player)

    context = {
        'role': role,
        'level': level + 1,
        'hp': hp,
        'atk': atk,
        'defe': defe,
        'progress': str(Player.objects.get(id = request.session['id']).exp * 100 / (5 + 2 * level)),
        's1_name': s1_name,
        's1_desc': s1_desc,
        's2_name': s2_name,
        's2_desc': s2_desc,
        's3_name': s3_name,
        's3_desc': s3_desc,
        's4_name': s4_name,
        's4_desc': s4_desc,
        'player': Player.objects.get(id = request.session['id']),
        'friends': Player.objects.get(id = request.session['id']).friends.order_by('username'),
        'recent_games': Player.objects.get(id = request.session['id']).games.order_by('-id')[:3],
        'recent_players': recent_players,
    }
    return render(request, 'login/main.html', context)

def search(request):
    friends_id = []
    for friend in Player.objects.get(id = request.session['id']).friends.all():
        friends_id.append(friend.id)
    players = Player.objects.filter(username__startswith = request.POST['search']).exclude(id = request.session['id']).exclude(id__in = friends_id).order_by('username')
    return render(request, 'login/search.html', { 'players': players })

def add_friend(request):
    if request.method == 'POST':
        p = Player.objects.get(id = request.session['id'])
        p.friends.add(Player.objects.get(id = int(request.POST['player_id'])))
        p.save()
        return redirect('/main')
    else:
        return redirect('/')

def display_player(request, num):
    username = Player.objects.get(id = num).username
    role_id = Player.objects.get(id = num).role
    level = Player.objects.get(id = num).level - 1
    if role_id == 1:
        role = "Knight"
        hp = 50 + 5 * level
        atk = 4 + 2 * level
        defe = 10 + 4 * level
        s1_name = "Shield Wall"
        s1_desc = "Reduce damage taken from the enemy for a few turns. CD: 4"
        s2_name = "War Cry"
        s2_desc = "Attracts the enemy's attention and forces him/her to use only basic attack for a few turns. CD: 6"
        s3_name = "Crippling Blows"
        s3_desc = "Your normal attacks cripple the enemy, reducing their damage and stacks up to 5 times. CD: 6"
        s4_name = "Revenge"
        s4_desc = "Deal equal damange taken from an enemy back at the enemy for the next turn. CD: 3"

    elif role_id == 2:
        role = "Rogue"
        hp = 30 + 3 * level
        atk = 10 + 4 * level
        defe = 5 + 3 * level
        s1_name = "Poisoned knife"
        s1_desc = "Hurls a poisoned knife at the target. Deals damage over a few turns.. CD: 5"
        s2_name = "Paralytic Knife"
        s2_desc = "Throw a knife coated in a toxin that renders its victim helpless for a few turns. CD: 4"
        s3_name = "Expose Weakness"
        s3_desc = "If the enemy has an effect, youe next attack deals massive damage. CD: 7"
        s4_name = "Shadowstep"
        s4_desc = "Greatly increases dexterity and greatly increases damage of your next attack. CD: 5 "

    elif role_id == 3:
        role = "Mage"
        hp = 30 + 3 * level
        atk = 10 + 4 * level
        defe = 3 + 2 * level
        s1_name = "Fireball"
        s1_desc = "Launches a fireball at your enemy and burn them for a few turns. CD: 4"
        s2_name = "Blizzard"
        s2_desc = "Lowers the enemy attack and freezes the enemy for a few turns. CD: 4"
        s3_name = "Mage Shield"
        s3_desc = "Recovers some lost hp in the form of shield. CD: 4"
        s4_name = "Teleport"
        s4_desc = "Greatly increases evasiveness for the next few turns. CD: 8"

    elif role_id == 4:
        role = "Ranger"
        hp = 30 + 3 * level
        atk = 7 + 5 * level
        defe = 4 + 2 * level
        s1_name = "Aimed Shot"
        s1_desc = "A precisely aimed shot which deals more damage the less heatlh the enemy has. CD: 3"
        s2_name = "Vile Bolt"
        s2_desc = "A poisoned arrow which deals containuous damage and leaves the victim with less defense. CD: 5"
        s3_name = "Secret Trap"
        s3_desc = "A trap that lowers the enemy defense and lasts for 2 turns. Triggers whenever the enemy uses active skills. CD: 6"
        s4_name = "Apollo Strike"
        s4_desc = "A burtal shot that leaves the enemy unconscious for 2 turns. Only works if the enemy has less health than you. CD: 7"

    elif role_id == 5:
        role = "Beserker"
        hp = 40 + 4 * level
        atk = 7 + 3 * level
        defe = 6 + 3 * level
        s1_name = "Enrage"
        s1_desc = "Increasing damage dealt AND taken for a few turns. CD: 5"
        s2_name = "Death Wish"
        s2_desc = "Take away a portion of youe health and deal massive damage to the enemy. CD: 3"
        s3_name = "Bloodthirsty"
        s3_desc = "Your next few attacks recovers some of your HP based on your damage. CD: 6"
        s4_name = "Adrenaline Rush"
        s4_desc = "Your attack is increased for the next few turns and also apply a bleeding effect. CD: 5"

    recent_players = []
    for game in Player.objects.get(id = num).games.order_by('-id')[:3]:
        for player in game.players.all():
            if player.id != int(num):
                recent_players.append(player)

    context = {
        'username': username,
        'role': role,
        'level': level + 1,
        'hp': hp,
        'atk': atk,
        'defe': defe,
        'progress': str(Player.objects.get(id = request.session['id']).exp * 100 / (5 + 2 * level)),
        's1_name': s1_name,
        's1_desc': s1_desc,
        's2_name': s2_name,
        's2_desc': s2_desc,
        's3_name': s3_name,
        's3_desc': s3_desc,
        's4_name': s4_name,
        's4_desc': s4_desc,
        'player': Player.objects.get(id = num),
        'friends': Player.objects.get(id = num).friends.order_by('username'),
        'recent_games': Player.objects.get(id = num).games.order_by('-id')[:3],
        'recent_players': recent_players,
    }
    return render(request, 'login/display_player.html', context)

def logout(request):
    if request.method == 'POST':
        request.session.clear()
        return redirect('/')
    else:
        return redirect('/') 

def start_game(request):
    if request.method == 'POST': 
        your_games = Player.objects.get(id = request.session['id']).games.all()
        for game in your_games:
            for player in game.players.all():
                if player.id == int(request.POST['enemy_id']):
                    request.session['enemy_id'] = request.POST['enemy_id']
                    return redirect(f'/game_sess/{game.id}')

        you = Player.objects.get(id = request.session['id'])
        enemy = Player.objects.get(id = request.POST['enemy_id'])
        request.session['enemy_id'] = request.POST['enemy_id']
        your_name = you.username
        enemy_name = enemy.username

        if you.role == 1:
            your_health = 50 + 5 * (you.level - 1)
        elif you.role == 2:
            your_health = 30 + 3 * (you.level - 1)
        elif you.role == 3:
            your_health = 30 + 3 * (you.level - 1)
        elif you.role == 4:
            your_health = 30 + 3 * (you.level - 1)
        elif you.role == 5:
            your_health = 40 + 4 * (you.level - 1)

        if enemy.role == 1:
            enemy_health = 50 + 5 * (enemy.level - 1)
        elif enemy.role == 2:
            enemy_health = 30 + 3 * (enemy.level - 1)
        elif enemy.role == 3:
            enemy_health = 30 + 3 * (enemy.level - 1)
        elif enemy.role == 4:
            enemy_health = 30 + 3 * (enemy.level - 1)
        elif enemy.role == 5:
            enemy_health = 40 + 4 * (enemy.level - 1)

        g = Game(creator = you, joiner = enemy, creator_health = your_health, member_health = enemy_health, creator_frz = False, member_frz = False, creator_brn = False, member_brn = False, creator_pos = False, member_pos = False, battleground = 1)
        g.save()
        g_obj = Game.objects.get(id = g.id)
        g_obj.players.add(you)
        g_obj.players.add(enemy)
        g_obj.save()
        return redirect(f'/game_sess/{ g.id }')
    else:
        return redirect('/') 

def cont_game(request):
    pass

def game_sess(request, id):
    your_name = Game.objects.get(id = id).players.get(id = request.session['id']).username
    your_role_id = Game.objects.get(id = id).players.get(id = request.session['id']).role
    your_level = Game.objects.get(id = id).players.get(id = request.session['id']).level
    if request.session['id'] == Game.objects.get(id = id).creator.id:
        your_health = Game.objects.get(id = id).creator_health
        enemy_health = Game.objects.get(id = id).member_health
    else:
        your_health = Game.objects.get(id = id).member_health
        enemy_health = Game.objects.get(id = id).creator_health
    enemy_name = Game.objects.get(id = id).players.get(id = request.session['enemy_id']).username
    enemy_role_id = Game.objects.get(id = id).players.get(id = request.session['enemy_id']).role
    enemy_level = Game.objects.get(id = id).players.get(id = request.session['enemy_id']).level

    if your_role_id == 1:
        your_role = "Knight"
        s1_name = "Shield Wall"
        s2_name = "War Cry"
        s3_name = "Crippling Blows"
        s4_name = "Revenge"
    elif your_role_id == 2:
        your_role = "Rogue"
        s1_name = "Poisoned knife"
        s2_name = "Paralytic Knife"
        s3_name = "Expose Weakness"
        s4_name = "Shadowstep"
    elif your_role_id == 3:
        your_role = "Mage"
        s1_name = "Fireball"
        s2_name = "Blizzard"
        s3_name = "Mage Shield"
        s4_name = "Teleport"
    elif your_role_id == 4:
        your_role = "Ranger"
        s1_name = "Aimed Shot"       
        s2_name = "Vile Bolt"
        s3_name = "Secret Trap"
        s4_name = "Apollo Strike"
    elif your_role_id == 5:
        your_role = "Beserker"
        s1_name = "Enrage"
        s2_name = "Death Wish"
        s3_name = "Bloodthirsty"
        s4_name = "Adrenaline Rush"

    if enemy_role_id == 1:
        enemy_role = "Knight"
    elif enemy_role_id == 2:
        enemy_role = "Rogue"
    elif enemy_role_id == 3:
        enemy_role = "Mage"
    elif enemy_role_id == 4:
        enemy_role = "Ranger"
    elif enemy_role_id == 5:
        enemy_role = "Beserker"

    context = {
        'your_name': your_name,
        'your_role': your_role,
        'your_level': your_level,
        'your_health': your_health,
        'enemy_name': enemy_name,
        'enemy_role': enemy_role,
        'enemy_level': enemy_level,
        'enemy_health': enemy_health,
        's1_name': s1_name,
        's2_name': s2_name,
        's3_name': s3_name,
        's4_name': s4_name,
    }
    return render(request, 'login/game.html', context)

def attack(request):
    if request.method == 'POST':
        return redirect('/main')
    else:
        return redirect('/')

def leave(request):
    if request.method == 'POST':
        return redirect('/main')
    else:
        return redirect('/')