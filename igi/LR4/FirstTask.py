import pickle
import csv

#Creator Mikhail Kupreichyk from group 253503
#version 1
#Lab number 4
#08.05.2024
#Variant 14
class Tree:
    """Class tree with counting trees(healthy and all) in all forest."""
    Forest_pop = 0 #Static attribute

    Forest_healthy_trees = 0 #Static attribute

    def __init__(self, tree_type):
        self.tree_type = tree_type

    @classmethod
    def get_forest_pop(cls):
        """Getting all tree pop in forest."""
        return cls.Forest_pop

    @classmethod
    def get_forest_healthy_trees(cls):
        """Getting all healthy tree pop in forest."""
        return cls.Forest_healthy_trees

    @classmethod
    def get_forest_sick_trees(cls):
        """Getting all sick tree pop in forest."""
        return cls.Forest_pop - cls.Forest_healthy_trees

    def __str__(self):
        return f"This forest_plot consist of {self.tree_type} trees"

class MixinForestPlot:
    """Mixin for ForestPlot_Pop"""
    def __init__(self, ForestPlot_Pop): #Using Mixin to add attribute ForestPlot_Pop
        self.ForestPlot_Pop = ForestPlot_Pop

class ForestPlot(Tree, MixinForestPlot):
    """Class that represents segment of forest with same type of trees."""
    def __init__(self, tree_type, ForestPlot_Pop, ForestPlot_healthy_trees, forestplot_name):
        super().__init__(tree_type) #Using super()
        MixinForestPlot.__init__(self, ForestPlot_Pop)
        self.ForestPlot_healthy_trees = ForestPlot_healthy_trees

        Tree.Forest_pop += self.ForestPlot_Pop
        Tree.Forest_healthy_trees += self.ForestPlot_healthy_trees

        self.forestplot_name = forestplot_name

    @property #Getter
    def forestPlot_Pop(self):
        return self.ForestPlot_Pop

    @forestPlot_Pop.setter #Setter
    def forestPlot_Pop(self, val):
        Tree.Forest_pop -= self.ForestPlot_Pop
        Tree.Forest_pop += val
        self.ForestPlot_Pop = val

    @property
    def forestPlot_healthy_trees(self):
        return self.ForestPlot_healthy_trees

    @property
    def forestPlot_sick_trees(self):
        return self.forestPlot_Pop - self.ForestPlot_healthy_trees

    @property
    def relative_num_sick_trees_percent(self):
        return (Tree.get_forest_sick_trees() / Tree.Forest_pop * 100)

    @property
    def forestPlot_name(self):
        return self.forestplot_name

    @property
    def tree_Type(self):
        return self.tree_type

    def __str__(self): #Magic method
        return (f"Name of plot in forest: {self.forestPlot_name()}, population: {self.forestPlot_Pop}, number of "
                f"healthy trees: {self.forestPlot_healthy_trees()}, number of sick trees: "
                f"{self.forestPlot_sick_trees()}.")

class ForestDataHandler:
    """Class that represent Forest(like list of ForestPlots) consist of ForestPlots."""
    def __init__(self):
        self.Forest = []
    def deserialize_from_dict(self, forestPlot_dict):
        """Deserialize dictionary to list and save list in attribute."""
        self.Forest = []
        for forestPlot_data in forestPlot_dict.values():
            forestPlot = ForestPlot(**forestPlot_data)
            self.Forest.append(forestPlot)

    def add_forestPlot(self, forestPlot):
        """Method for adding ForestPlot to list attribute."""
        self.Forest.append(forestPlot)

    def serialize_pickle(self, filename):
        """Serialize list and save in file, using pickle."""
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.Forest, file)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def deserialize_pickle(self, filename):
        """Deserialize file and save in list, using pickle."""
        try:
            with open(filename, 'rb') as file:
                self.Forest = pickle.load(file)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def serialize_csv(self, filename):
        """Serialize list and save in file, using csv."""
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['tree_type', 'ForestPlot_Pop', 'ForestPlot_healthy_trees', 'forestplot_name']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for ForestPlot in self.Forest:
                    writer.writerow({'tree_type': ForestPlot.tree_Type, 'ForestPlot_Pop': ForestPlot.forestPlot_Pop,
                                     'ForestPlot_healthy_trees': ForestPlot.forestPlot_healthy_trees,
                                     'forestplot_name': ForestPlot.forestPlot_name})
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    def deserialize_csv(self, filename):
        """Deserialize file and save in list, using csv."""
        try:
            self.Forest = []
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    NewForestPlot = ForestPlot(row['tree_type'], int(row['ForestPlot_Pop']),
                                      int(row['ForestPlot_healthy_trees']),
                                      row['forestplot_name'])
                    self.Forest.append(NewForestPlot)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def input_forestPlot_info(self):
        """Method for inputting from console and save in list attribute."""
        while True:
            try:
                forestplot_name = input("Enter name of plot in forest: ")
                tree_type = input("Enter tree type: ")
                population = (int)(input("Population in forestplot: "))
                healthy_trees = (int)(input("Number of healthy trees in forestplot: "))

                if(population <= 0 or healthy_trees > population or healthy_trees <= 0):
                    print("ERROR! Input error occured!")
                    continue
                else:
                    break
            except ValueError:
                print("ERROR! Input error occured!")
                continue

        forestPlot = ForestPlot(tree_type, population, healthy_trees, forestplot_name)
        self.Forest.append(forestPlot)


    def num_of_sick_trees_on_all_types(self):
        """Print number of sick trees on all tree type."""
        types = {ForestPlot.tree_Type for ForestPlot in self.Forest}

        sick = 0

        pop = 0

        for treetype in types:
            for forestPlot in [forestPlot for forestPlot in self.Forest if forestPlot.tree_Type == treetype]:
                sick += forestPlot.forestPlot_sick_trees
                pop += forestPlot.forestPlot_Pop

            if (sick == 0):
                print(f"{treetype} has 0 sick trees.")
            else:
                print(f"{treetype} has % of sick/(number of all {treetype} trees) = {sick / pop}.")

            sick = 0
            pop = 0
    def num_of_trees_on_forestPlot(self, name):
        """Print number of trees on some sector that have name like in method argument."""
        list = [forestPlot for forestPlot in self.Forest if forestPlot.forestPlot_name == name]

        if(len(list) > 0):
            for forestplot in list:
                print(f"{forestplot.forestPlot_name} has num of trees = {forestplot.forestPlot_Pop}.")
        else:
            print(f"{name} does not exist.")
    def information_of_tree_type(self, tree_type):
        """Prints all information about tree that have same type like in args."""

        list = [forestPlot for forestPlot in self.Forest if forestPlot.tree_Type == tree_type]

        pop = 0

        sick = 0

        healthy = 0

        type = ""

        for forestPlot in list:
            type = forestPlot.tree_Type
            pop += forestPlot.forestPlot_Pop
            sick += forestPlot.forestPlot_sick_trees
            healthy += forestPlot.forestPlot_healthy_trees

        print(f"{type} has num of trees = {pop}, number of sick = {sick}, number of healthy = {healthy}.")

    def sort_by_type(self):
        """Method thar return sort list attribute by tree type."""
        sorted_forest = sorted(self.Forest, key=lambda ForestPlot: ForestPlot.tree_Type)
        return sorted_forest

    def search_by_plot(self, name_of_plot):
        """Method thar return searched segment in list attribute by name of segment."""
        list = [forestPlot for forestPlot in self.Forest if forestPlot.forestPlot_name == name_of_plot]
        return list

    def search_by_type(self, tree_type):
        """Method thar return searched tree type in list attribute by name of tree type."""
        list = [forestPlot for forestPlot in self.Forest if forestPlot.tree_Type == tree_type]
        return list
def main():
    while True:
        handler = ForestDataHandler()

        forestPlot_dict = {
            '1': {'tree_type': 'береза', 'ForestPlot_Pop': 10, 'ForestPlot_healthy_trees': 5, 'forestplot_name': '1'},
            '2': {'tree_type': 'береза', 'ForestPlot_Pop': 20, 'ForestPlot_healthy_trees': 10, 'forestplot_name': '2'},
            '3': {'tree_type': 'ель', 'ForestPlot_Pop': 30, 'ForestPlot_healthy_trees': 15, 'forestplot_name': '3'}
        }

        handler.deserialize_from_dict(forestPlot_dict)

        forestPlot = ForestPlot('дуб', 12, 3, '3')

        handler.add_forestPlot(forestPlot)

        handler.input_forestPlot_info()

        handler.num_of_trees_on_forestPlot('1')

        handler.num_of_sick_trees_on_all_types()

        handler.information_of_tree_type('береза')

        print(f"All trees in forest: {Tree.Forest_healthy_trees}")

        handler.serialize_csv("D:\\253503_KUPREICHYK_14\igi\\1csv.txt")

        handler.deserialize_csv("D:\\253503_KUPREICHYK_14\igi\\1csv.txt")

        handler.serialize_pickle("D:\\253503_KUPREICHYK_14\igi\\1pickle.txt")

        handler.deserialize_pickle("D:\\253503_KUPREICHYK_14\igi\\1pickle.txt")

        print("to exit enter e")

        if input() == 'e':
            break

if(__name__ == "__main__"):
    main()