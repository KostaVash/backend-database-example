from google.cloud import datastore
import db_manager.undoredomanager as urm

"""
DB_Manager class
this class will interact with the DB
basic operations like get,set and queries 
this class will save all the set/unset operations to support undo/redo functionality 
"""


class DB_Manager:
    def __init__(self):
        self.db = datastore.Client()
        self.urm = urm.UndoRedoManager()

    def set_entity(self, name, value, flag):
        """
        saves the item info, name and value, and if the flag is true stores the function info in UndoRedoManager
        :param name: the name of the item
        :param value: the value of the item
        :param flag: if pass it to UndoRedoManager
        :return: True
        """
        entity = datastore.Entity(key=self.db.key('item', name))
        entity.update(
            {'name': name,
             'value': value})
        if flag:
            prev_value = self.get_entity(name)
            self.urm.write(self.set_entity, name, value, prev_value)
        self.db.put(entity)
        return True

    def get_entity(self, name_):
        """
        finds the item value by his name
        :param name_: the name of the item
        :return: the value of the item or None if not found
        """
        query = self.db.query(kind='item')
        name = list(query.add_filter('name', '=', name_).fetch(1))
        if name:
            n_name = dict(name[0])
            res = str(n_name['value'])
            return res
        return 'None'

    def unset_entity(self, name, flag):
        """
        changes the item value to None
        :param name: the name of the item
        :param flag: True to save in UndoRedoManager, else skip
        :return: the value of the item
        """
        if flag:
            prev_value = self.get_entity(name)
            self.urm.write(self.unset_entity, name, 'None', prev_value)
        ans = self.set_entity(name, 'None', False)
        if ans:
            return self.get_entity(name)
        else:
            return False

    def count_values(self, value):
        """
        return how many items we have with the same value
        :param value: the value we want to search
        :return: the number of items  with the same value
        """
        query = self.db.query(kind='item')
        ans = list(query.add_filter('value', '=', value).fetch())
        if ans:
            return len(ans)
        return 0

    def do_undo(self):
        """
        undo operation
        :return: the name and the value of the item after undo
        """
        func, name, value = self.urm.get_undo()
        if not func:
            return None, None
        func(name, value, False)
        return name, value

    def do_redo(self):
        """
        redo operation
        :return: the name and the value of the item after redo
        """
        func, name, value = self.urm.get_redo()
        if not func:
            return None, None
        func(name, value, False)
        return name, value

    def end(self):
        """
        deletes all instances of item from the database
        """
        query = self.db.query(kind='item')
        entities = list(query.fetch())
        for entity in entities:
            self.db.delete(entity.key)
