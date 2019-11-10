import random
import glob
import json
import urllib.request
import random

class Database:
    
    """
        Constructor Database
        
        Only one instance is created
        @params none
        @returns None
        """  
    def __init__(self):
        self.Fulllist = []
        self.pubBook = {}
        
    """
    Loops through local Json Files containing the dictionaries of each food item
    An instance of the food class is created for every food
    The List of food cakked Fulllist is populated
    
    @params 
    @returns None
    """    
    def scrape(self):
        for filename in glob.glob("JsonFiles/*.json"):
            raw = open(filename, "r")
            data = json.loads(raw.read())
                   
            section = data["molecules"]
            item_name = data["entity_alias_readable"].lower()
            category = data["category_readable"]
            #print(item_name)
                        
            List_of_molecules = []
            for flavor in section:
                for key in flavor:
                    if (key == "pubchem_id"):
                        List_of_molecules.append(flavor[key])    
                        
            CurrentItem = Food(item_name, List_of_molecules, category)
            self.Fulllist.append(CurrentItem)
            self.analyzeIngredients(CurrentItem, List_of_molecules)
     
"""
                Inserts an ingredient into all of the pubchems that it contains
                Before code is ran food is not in any of the pubchem classes
                
                
                @params Food item, the newly created food that has. list of pubchem items
                @returns None
                """ 
    def analyzeIngredients(self, wholeIngredient, List_of_molecules):
        for pubchemNum in List_of_molecules:
            if (str(pubchemNum) in self.pubBook):
                #print("Already exist")
                temp = self.pubBook[str(pubchemNum)]
                temp.add(wholeIngredient.getName())
            else:
                #print("Making a new one")
                emptylist = []
                newChem = pubchem(str(pubchemNum), emptylist)
                newChem.add(wholeIngredient.getName())
                self.pubBook[str(pubchemNum)] = newChem
                
 """
        Returns whether or not a molecule already exists inside the pubchem list
        If the molecule does not exist the pubchem is created then added to the list in another method
    
    @params string name
    @returns None
    """
    def has(self, moleculestring):
        for items in self.pubBook:
            if (items.getName() == moleculestring):
                return -1
        return 0
    

"""
    
    
    @params string name
    @returns None
    """
    def get_ingredient(self, food_name):
        ingredient = None
        for item in self.Fulllist:
            if food_name == str(item):
                #print(food_name + " is " + str(item))
                #print("Found " + str(item.getName()))
                #print(str(item) + " is present1")
                ingredient = item
        if ingredient is None:
            for item in self.Fulllist:
                if (item.getName() in food_name):
                    ingredient = item
                    #print(str(item) + " is present2")
                elif (food_name in item.getName()):
                    ingredient = item
                    #print(str(item) + " is present3")
        return ingredient
    
"""
        Returns whether or not a molecule already exists inside the pubchem list
        If the molecule does not exist the pubchem is created then added to the list
        
        @params string name
        @returns None
        """
    def get_pubchem(self, pub_string):
        return self.pubBook[str(pub_string)]

class Food:
   
 """
        Constructor for the Food class
        
        @params string name, list of pubchem in strings, string categor of food
        @returns None
        """ 
    def __init__(self, name, items, category):
        self.Listofchem = items
        self.name = name
        self.cat = category
        
"""
            Returns the list of pubchems contained inside the food
            
            @params none
            @returns A list of all of the chemicals inside the Food
            """            
    def getList(self):
        return self.Listofchem
    
 """
        Returns the name of the food
        
        @params none
        @returns string of food name
        """  
    def getName(self):
        return self.name  
"""
        A toString method for the Food class
           
        @params none
        @returns string name
        """  
    def __repr__ (self):
        return self.name 
        #+ " has " + str(len(self.Listofchem)) + " items"
        
        
"""
            Compares one food to another
            Helps see the similarties in molecular make up
            
            @params instance of food that will be compared
            @returns double, a grade that shows how similar the two moleculars are
            """ 
    def compare(self, otherFood):
        original = set(self.Listofchem)     
        try:
            new = set(otherFood.getList())
            numerator = original.intersection(new)
            percent = len(numerator) / len(original)
        except:
            percent = 0
        return percent

class pubchem:
    
    """
        Constructor for the pubchem class
        
        @params integer of the pubchem number, An empty list of the foods that have the current pubchem
        @returns None
        """  
    def __init__(self, name, ItemsWith):
        self.name = name
        self.Items = ItemsWith

"""
            Returns the name of the pubchem
            
            @params 
            @returns String name
            """        
    def getName(self):
        return self.name
    
"""
        Returns the listof Items that shuld contain a list of all the foods that have the following pubchem
        
        @params none
        @returns None
        """         
    def getCurrentIngredients(self):
        return self.Items

"""
        Adds the string passed in to the list of foods with the pubchem
        @params string name that will be added to the list
        @returns None
        """ 
    def add(self, newIngredient):
        self.Items.append(newIngredient)
"""
            A comparator for the pubchem class
            
            @params string name
            @returns boolean, whether or not the name matches the pubchem
            """          
    def __eq__ (self, other):
        if (self.name == other):
            return True
        return self.name == other.name
    
    def __repr__ (self):
        return (self.name + " has " + str(len(self.Items)) + " Foods with the chemical")

class Recipe:
    def __init__(self, name = None, database = None, foods = None):
        self.foods = foods
        self.list_of_chem = []
        for food in self.foods:
            if food is not None:
                self.list_of_chem += list(set(food.getList() + self.list_of_chem))
        self.name = name
        self.recipe_size_lmt = 15
        self.base_foods = ["butter", "sugar", "salt", "vanilla", "egg", "flour"]
        self.database = database
        for food_n in self.base_foods:
            self.add_food_db(food_n)

    """
                Returns the list of ingredients/foods in the recipe

                @returns array, the ingredient list
                """
    def get_foods(self):
        return self.foods

    """
                Returns the list of pubchems in the recipe

                @returns array, the pubchem list
                """
    def get_chems(self):
        return self.list_of_chem

    """
                Returns the recipe name

                @returns string, recipe name
                """
    def get_name(self):
        return self.name

    """
                Returns the worst food/ingredient in the recipe, according to the one that shares the least elements
                with the others

                @returns Food, the least compatible food
                """
    def get_worst_food(self):
        rating_list = []
        least_important = None
        index = 0
        for food in self.foods:
            try:
                if food.getName() in self.base_foods:
                    next
                food_score = 0.0
                for other_food in self.foods:
                    food_score += food.compare(other_food)
                rating_list.append(food_score)
                if least_important is None:
                    least_important = index
                else:
                    if rating_list[least_important] > food_score:
                        least_important = index
            except:
                print()
            finally:
                index += 1
        return self.foods[least_important]

    """
                Returns the best food in the recipe, according to the one thats most compatible/
                shares the most elements with the other elements.

                @returns Food, the most compatible food
                """
    def get_best_food(self):
        rating_list = []
        most_important = None
        index = 0
        for food in self.foods:
            food_score = 0.0
            for other_food in self.foods:
                food_score += food.compare(other_food)
            rating_list.append(food_score)
            if most_important is None:
                most_important = index
            else:
                if rating_list[most_important] < food_score:
                    most_important = index
            index += 1
        return self.foods[most_important]

    """
                A variant of the get_food function that excludes base food elements from the search

                @returns Food, the most compatible food
                """
    def get_best_food_var(self):
        rating_list = []
        most_important = None
        index = 0
        for food in self.foods:
            if food.getName() in self.base_foods:
                next
            food_score = 0.0
            for other_food in self.foods:
                food_score += food.compare(other_food)
            rating_list.append(food_score)
            if most_important is None:
                most_important = index
            else:
                if rating_list[most_important] < food_score:
                    most_important = index
            index += 1
        return self.foods[most_important]

    """
                Adds a new food to the ingredient list, using an entered food.

                @params Food, new food
                """
    def add_food(self, new_food):
        if new_food is not None:
            self.foods.append(new_food)
            self.foods = list(set(self.foods))
            self.list_of_chem = list(set(new_food.getList() + self.list_of_chem))

    """
                Adds a food using an entered food name, that is used to retrieve the cited food
                from the recipe's database, before the food is added to the recipe

                @params string, food name
                """
    def add_food_db(self, food_name):
        new_food = self.database.get_ingredient(food_name)
        self.add_food(new_food)

    """
                Removes a food and its relevant pubchems from the recipe using the food's name as
                input

                @params string, food name
                """
    def remove_food(self, food_name):
        try:
            deleted_food = None
            for food in self.foods:
                
                if food_name  == food.getName():
                    deleted_food = food
                    self.foods.remove(food)
            # removes any molecules that the deleted food has, that none of the remaining foods can account for.
            if deleted_food is not None:
                self.list_of_chem.clear()
                for food in self.foods:
                    self.list_of_chem = list(set(food.getList() + self.list_of_chem))
                # for chem in deleted_food.getList():
                #     remaining_food_has_chem = False
                #     for ingred in chem.getCurrentIngredients():
                #         if ingred in self.foods:
                #             remaining_food_has_chem = True
                #     if remaining_food_has_chem is False:
                #         self.list_of_chem.remove(chem)
        except:
                print()

    """
                A cleanup function that deletes foods with with None values from the ingredient list.
                
                @param Food, food being checked

                """
    def delete_none(self, food):
        if (food == None):
            self.foods.remove(food)

    """
                Checks whether a given food name is present within the ingredient list.

                @params string, food name
                @returns boolean, whether or not the food is present
                """
    def check_food(self, food_name):
        food_present = False
        for food in self.foods:
            if food.getName() == food_name:
                food_present = True
        return food_present

    """
                Sums the parity total parity of the recipe by iterating through the recipe, and summing
                elements' parities with one another.

                @returns float, the total parity of the recipe
                """
    def rate_parity_total(self):
        total_rating = 0
        for food in self.foods:
            food_score = 0.0
            for other_food in self.foods:
                try:
                    food_score += food.compare(other_food)
                except:
                    food_score += 0
            total_rating += food_score
        return total_rating

    """
                Returns the average parity, using the length of the ingredient list.

                @returns float, the average parity of the recipe
                """
    def rate_parity_avg(self):
        return self.rate_parity_total()/len(self.foods)

    """
                Compares the pubchem list of the recipe to the pubchems in a given food, returning their parity.

                @params Food, other food
                @returns float, parity/percentage similarity of the two.
                """
    def compare_food(self, other_food):
        original = set(self.list_of_chem)

        new = set(other_food.getList())
        numerator = original.intersection(new)
        percent = len(numerator) / len(original)
        return percent

    """
                    Compares the ingredient list of the recipe to the ingredients in another 
                    recipe, returning their similarity.

                    @params Food, other food
                    @returns float, percentage similarity of the two.
                    """
    def compare_recipe_foods(self, other_recipe):
        original = set(self.foods)
        new = set(other_recipe.get_foods())
        numerator = original.intersection(new)
        percent = len(numerator) / len(original)
        return percent

    """
                    A cleanup function that ensures the recipe is at the correct length, and that
                    the base ingredients are all present.

                    """
    def verify(self):
        for food_name in self.base_foods:
            if self.check_food(food_name) is False:
                self.add_food_db(food_name)
        while len(self.foods) > self.recipe_size_lmt:
            self.remove_food(self.get_worst_food())

    """
                    A mutation that replaces a random ingredient in the recipe with another random ingredient,
                    based on its pubchem list.

                    """
    def mutate_replace_random(self):
        removed_food_name = "Butter"
        while removed_food_name not in self.base_foods:
            removed_food_name = random.choice(self.foods).getName()
        self.remove_food(removed_food_name)
        rem_food = self.database.get_ingredient(removed_food_name)
        rem_chem_list = rem_food.getList()
        rand_chem = self.database.get_pubchem(random.choice(rem_chem_list))
        new_food_name = random.choice(rand_chem.getCurrentIngredients())
        self.add_food_db(new_food_name)
        self.verify()

    """
                A mutation that adds a new ingredient based on the randomly selecting a linked ingredient
                from the best ingredient's pubchem list.
                """
    def mutate_add_from_best(self):
        rand_best_chem = random.choice(self.get_best_food().getList())
        rand_best_chem = self.database.get_pubchem(rand_best_chem)
        self.add_food_db(random.choice(rand_best_chem.getCurrentIngredients()))
        self.verify()

    """
                A mutation that removes the worst ingredient from the recipe.
                """
    def mutate_remove_worst(self):
        self.remove_food(self.get_worst_food().getName())

    """
                A defunct fitness function that decreases total parity based on the highest similarity of the 
                the recipe to a given list of recipes.
                
                @param array, other recipes for checking novelty
                @returns float, final fitness
                """
    def rate_fitness(self, other_recipes):
        strongest_match_parity = 0
        for recipe in other_recipes:
            if self.compare_recipe_foods(recipe) > strongest_match_parity:
                strongest_match_parity = self.compare_recipe_foods(recipe)
        return self.rate_parity_total() - (self.rate_parity_total() * strongest_match_parity)

    """
                A function that generates a new name for the recipe.
                """
    def gen_new_name(self):
        adjectives = open("english-adjectives.txt", 'r')
        ends = open("soup-synonyms.txt", 'r')
        adjective_list = []
        ends_list = []
        for adj in adjectives:
            adjective_list.append(adj)
        for end in ends:
            ends_list.append(end)
        #print("go")
        #Feel free to delete, I kept getting a concatenation error so I casted everything
        #print(isinstance(random.choice(adjective_list).rstrip(), str))
        #part1 = random.choice(adjective_list).rstrip()
        #print(isinstance(random.choice(list(self.ingredients_dict)).getIngredient(), str))
        #part2 = random.choice(list(self.ingredients_dict)).getIngredient()
        #print(isinstance(random.choice(list(self.ingredients_dict)).getIngredient(),str))
        #part3 = random.choice(list(self.ingredients_dict)).getIngredient()
        #print(isinstance(random.choice(ends_list), str))
        #part4 = random.choice(ends_list)
        #new_name = part1 + " " + part2 + " & " + part3 + " " + part4
        new_name = str(random.choice(adjective_list).rstrip()) + " " + str(random.choice(self.foods).getName()) + " & " + str(random.choice(self.foods).getName()) + " " + str(random.choice(ends_list))

        self.name = new_name
        return new_name    
        
def main():
    ing = []
    rec = []
    db = Database()
    db.scrape()
    rec = parse_startup(ing, rec, db)    
        
    starter_recipes = randomRecipeGen(rec)
    
    for recipe in starter_recipes:
        for f in recipe.get_foods():
            recipe.delete_none(f)

    num_of_gens = 40
    for x in range(0, num_of_gens):
        rec = generation_production(starter_recipes, db)
        #print(rec)
        for r in rec:
            random_mutation(r)
            r.gen_new_name()
            
    print("Here is the list of recipes after " + str(num_of_gens) + " generations")
    for items in rec:
        print(items.get_name().title())
        print(items.rate_parity_total())
        print(items.get_foods())
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Final recipe:")
    print("-------------")
    nov_rec = []
    for i in rec:
        nov_rec.append(i.rate_parity_avg())
    
    max_nov = rec[nov_rec.index(max(nov_rec))]
    print((max_nov.get_name()).title())
    print(max_nov.rate_parity_total())
    for ing in max_nov.get_foods():
        print((ing.getName()).title())
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

"""
The function that parses the input file for all of the recipes to be used throughout the
rest of this project. It pulls both data for each recipe in addition to cataloguing all the ingredients found
in the input folder. 
@params set ingredients, the set of unique ingredients found in the given input file
@params list recipes, the list of recipes parsed from the input file 
@params  db, database with all the food and their chemical compositions
@returns recipes, the list of recipes for a given run
"""
def parse_startup(ingredients, recipes, database):
    infile = open('newcookies2.txt')
    data = infile.readlines()        
    
    count = 0   
    rec_ing = []
    for line in data:
        new_ing = ''
        split_line = line.split()
        if (len(split_line) >= 1 and checkInt(split_line[0][0]) == False):
            if (count != 0):
                for ing in rec_ing:
                    if (ing == None):
                        rec_ing.remove(ing)

                new_recipe = Recipe(recipe_name, database, rec_ing)
                recipes.append(new_recipe)
                rec_ing = []
            recipe_name = ' '.join(split_line)
            count += 1
         
        else:
            if ("/" not in line):
                new_ing = database.get_ingredient(' '.join(split_line[2:]))
                rec_ing.append(new_ing)
                ingredients.append(new_ing)
            elif ("/" in line):
                if (checkInt(split_line[0]) == True):
                    new_ing = database.get_ingredient(' '.join(split_line[3:]))
                else: 
                    new_ing = database.get_ingredient(' '.join(split_line[2:]))
                if (new_ing != None):
                    rec_ing.append(new_ing)
                    ingredients.append(new_ing) 
        
    return recipes

"""
A helper function for parse_startup(). Basically just checks wehter or not the string value
from the inputted text file can be converted to an int. If false, this insdicates that 
it is a string. 
    
@params x, string being checked
@return Boolean, true if x can be casted as a string
"""
def checkInt(x):
    try: 
        int(x)
        return True
    except ValueError:
        return False

"""
A function that cretes the starting generation of recipes by choosing 10 random recuoes from 
the list of recipes that were created throup parse_startup().
    
@params recipes, the array of the current population of recipes (Recipe objects)
@return subsection, a list of 10 recipes that represent the original generation of recipes
"""
def randomRecipeGen(recipes):
    subsection = []
    used_recipes = list(range(0, len(recipes)))
    
    count = 0
    while (count <= 10):
        chosen_rec = random.randint(0, len(recipes))
        if (chosen_rec in used_recipes):
            subsection.append(recipes[chosen_rec])
            count += 1
    return subsection

"""
The function that calls the crossover function proportional to the amount of recipes that exist, generating a
whole new population of recipes (or curret population). 
    
@params recipes, the array of the current population of recipes (Recipe objects)
        db, database with all the food and their chemical compositions
@returns new_gen, an array of a new generation of recipes that will replace the originally inputted recipes
"""
def generation_production(recipes, db):
    new_gen = [] 
    i = 0
    
    while i < len(recipes):
       
        new_gen.append(crossover(recipes, db))
        i+=1
    return new_gen

"""
The function that generates a new recipe by combining the first sub-list of the first recipe with the second 
sub-list of the second recipe, which are chosen based off of their fitness scores.
    
@params recipes, the array of the current population of recipes (Recipe objects)
        db, database with all the food and their chemical compositions
@returns new_recipe, a single recipe that was created from two parents of the inputted recipes
""" 
def crossover(recipes, db):
    empty = []
    new_recipe = Recipe(None, db, empty)
    
    parents_index = choose_recipe(recipes)
    
    first_parent = recipes[parents_index[0]]
    second_parent = recipes[parents_index[1]]    
    
    for i in range(0, min(len(first_parent.get_foods()), len(second_parent.get_foods()))):
    
        if (i == 0 or (i % 2)==0):
            new_recipe.add_food(first_parent.get_foods()[i])
        else: 
            new_recipe.add_food(second_parent.get_foods()[i])
            
    return new_recipe

"""
 The function that chooses which recipe is the fittest to be the parent of one of the recipes that will
 be apart of the new generation of recipes. The first parent is chosen based off 
 their fitness score of parity, but the second parent is randomized.
    
 @params recipes, the array of the current population of recipes (Recipe objects)
 @return chosen, the recipes who will be used to create a new recipe during crossover
"""
def choose_recipe(recipes):
    rec_fs = []
    parents = []
    
    for r in recipes: 
        rec_fs.append(r.rate_parity_avg())
        
    parents.append(rec_fs.index(max(rec_fs)))
    
    second = random.randint(0, len(recipes)-1)
    while (second == parents[0]):
        second = random.randint(0, len(recipes)-1)
    parents.append(second)
    return parents
    
"""
    Is called on every recipe after it is created
    Has a 20% of creating a mutation
    Every mutation has an equal chance of getting selected
    
    @params List of all of the ingredients
    @returns None
"""       
def random_mutation(rec):
                type_of_mutation = random.randint(1,15)

                if type_of_mutation == 1:
                    rec.mutate_replace_random()
        
                elif type_of_mutation == 2:
                    rec.mutate_add_from_best()
                   
                elif type_of_mutation == 3:
                    rec.mutate_remove_worst()
main()
