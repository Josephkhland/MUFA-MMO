import mufadb as db
import random 

class DescriptionGen:
    def __init__(self):
        self.fluff = ["sketchily-drawn", "rough", "minimalistic", "simple", "carefully-drawn", "hastily-drawn", "elaborate"]
        self.verbs = ["painted","engraved", "carved", "drawn", "glued", "scorched","stiched"] 
        self.position = ["the floor, adjacent to the", "the wall, adjacent to the", "the surface of the"]
        self.position_prefix = ["on", "upon", "over", "over a segment of"]
        self.adverb = ["hastily", "carefully", "roughly", "poorly", "artistically", "elaborately"]
        self.afterv = ["presented","expressed","delivered","demonstrated", "pictured", "illustrated"]
        pass

    def starts_with_vowel(self,s):
        try:
            vowels = ['a','e','i','o','u','y']
            if s[0] in vowels:
                return True
            else:
                return False 
        except:
            return None

    def insert_a_article(self,s):
        if self.starts_with_vowel(s):
            return "an "+ s
        else:
            return "a " + s

    def express_shape(self,s):
        synonyms = ["shape", "symbol"]
        shape_syn = random.choice(synonyms)
        return shape_syn+ " of " + self.insert_a_article(s)

    def enrich_shape(self,s):
        adj = random.choice(self.fluff)
        return adj + " " + self.express_shape(s)

    def diverse_action(self):
        adv = random.choice(self.adverb)
        v = random.choice(self.verbs)
        return adv + " " + v

    def state_position(self, t, suffix = ", "):
        p = random.choice(self.position)
        return p + " " + t + suffix

    def express_position(self, t, suffix = ", "):
        p = random.choice(self.position)
        pre = random.choice(self.position_prefix)
        return pre + " " + p + " " + t + suffix
    
    def interactable_description(self,tag,symbol):
        result : str
        b = " "
        choice = random.randint(0,5)

        if choice == 0:
            #String there is a + self.enrich_shape(s)
            result = random.choice(self.verbs) + b + self.express_position(tag)+"there is the " + self.enrich_shape(symbol) + "."
        elif choice ==1: 
            #String pre_enriched + ", there is the " + self.express_shape(s)
            result = self.diverse_action() + b + self.express_position(tag)+ "there is the " + self.express_shape(symbol) + "."
        elif choice ==2:
            #String pre_enriched + ", the " + self.express_shape(s) + " is expressed."
            result = self.diverse_action() + b + self.express_position(tag)+ "the " + self.express_shape(symbol) + " is " +random.choice(self.afterv) +"."
        elif choice ==3:
            #The surface of the {}, is occupied by the + self.enrich_shape(s)
            result = self.state_position(tag) + "is occupied by the " + self.enrich_shape(symbol) +"."
        elif choice ==4:
            #On the wall adjacent to the {}, the {symbol} is {enrich_action} painted
            result = self.express_position(tag)+"the " +self.express_shape(symbol) + " is " + self.diverse_action() +"."
        elif choice ==5:
            #The symbol of a sun is {diverse action} over the surface of the {}.
            result = "The "+ self.enrich_shape(symbol) + " is " + self.diverse_action() + b + self.express_position(tag, ".") 
        return result.capitalize()


def generateDescription():
    all_symbols = db.Tags.objects.get(name = "Symbols").collection
    all_decorators = db.Tags.objects.get(name = "Decorators").collection
    symbol = random.choice(all_symbols)
    decorator = random.choice(all_decorators)
    result = DescriptionGen().interactable_description(decorator,symbol)
    return result

def generateDescriptionTest(value):
    all_symbols = db.Tags.objects.get(name = "Symbols").collection
    all_decorators = db.Tags.objects.get(name = "Decorators").collection
    output = []
    for counter in range(value):
        symbol = random.choice(all_symbols)
        decorator = random.choice(all_decorators)
        result = DescriptionGen().interactable_description(decorator,symbol)
        output.append(result)
    return output

def gen_interactable_description(decorator,symbol):
    return DescriptionGen().interactable_description(decorator,symbol)


class ClueGen:
    def __init__(self):
        pass

    def starts_with_vowel(self,s):
        try:
            vowels = ['a','e','i','o','u','y']
            if s[0] in vowels:
                return True
            else:
                return False 
        except:
            return None

    def insert_a_article(self,s):
        if self.starts_with_vowel(s):
            return "an "+ s
        else:
            return "a " + s
    
    def dial_plus_symbol(self,dial_correct_value, symbol):
        output = dial_correct_value + symbol
        return output
    
    def tag_plus_symbol(self,tag, symbol):
        output = tag + symbol
        return output

    def tag_plus_dial(self,tag,dial_correct_value):
        output = tag + dial_correct_value
        return output