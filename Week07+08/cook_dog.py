#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: cook_dog.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
from abc import ABC, abstractmethod
from animals import Shape, Character, Food


class Animal(ABC):
    def __init__(self, food, shape, character):
        self._food = food
        self._shape = shape
        self._character = character

    def food(self):
        """
        eat meat --> eat glass --> both
        :return:
        """
        f = Food()
        f.type = self._food
        return f.type

    def shape(self):
        """
        slim --> medium --> fat
        :return:
        """
        s = Shape()
        s.shape = self._shape
        return s.shape

    def character(self):
        """
        gentle --> violent
        :return:
        """
        c = Character()
        c.character = self._character
        return c.character

    def _eat_child(self):
        if all(
                [
                    self.character() == 'violent',
                    self.shape() != 'slim',
                    self.food() == 'meat',
                    ]):
            return True

        return False

    @property
    @abstractmethod
    def dangerous(self):
        pass


class Zoo:
    def __init__(self, name):
        self.name = name
        self._data = []

    @property
    def data(self):
        return self._data

    def add_animal(self, animal: Animal):
        if animal in self._data:
            return

        if not hasattr(self, animal.__class__.__name__):
            setattr(self, animal.__class__.__name__, animal.__class__)

        self._data.append(animal)


class Cat(Animal):
    LAUGH = '我们一起学锚叫,一起miao miao miao miao miao~'

    def __init__(self, name, food, shape, character):
        super().__init__(food, shape, character)
        self._name = name

    def is_pet(self):
        return not self.dangerous

    @property
    def name(self):
        return self._name

    @property
    def dangerous(self):
        return self._eat_child()


class Dog(Cat):
    LAUGH = '小白,今年旺不旺? 小白:汪汪汪~'


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', 'meat', 'medium', 'violent')
    dog1 = Dog('大花狗 1', 'meat', 'slim', 'violent')
    dog2 = Dog('大花狗 2', 'meat', 'slim', 'violent')

    # 增加一只猫到动物园
    z.add_animal(cat1)
    z.add_animal(cat1)
    z.add_animal(dog1)
    z.add_animal(dog2)
    z.add_animal(dog1)
    for i in z.data:
        print(i.name, ': ', i.LAUGH, 'am i not a hello ketty? ', i.dangerous)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
    have_dog = hasattr(z, 'Dog')
    print(have_cat)
    print(have_dog)
