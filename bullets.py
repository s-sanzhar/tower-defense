class Bullet(object):
    def __init__(self, tower, target):
        self.shooter = tower
        self.target = target
        self.color = self.shooter.color

    def shoot(self):
        self.target.hp -= self.shooter.damage

