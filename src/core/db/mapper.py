from db import SQLite3
from  datetime import datetime

class BaseDatabaseObject(object):
    
    def __init__(self):
        self.db = SQLite3()
    
    def insert(self, table, data):
        k = [i for i in data]
        v = [data[i] for i in data]
        try:
            self.db.execute("insert into %s (%s) values (%s);" \
                % (table, ','.join(k), ','.join(['?' for i in v])), v)
        except:
            self.db.rollback()
            return 0
        self.db.commit()
        return 1
    
    def update(self, table, data, where):
        v = [k + "=?" for k in data]
        query = "update %s set %s where %s;" % \
            (table, ','.join(v), where[0])
        try:
            self.db.execute(query, tuple([data[k] for k in data]) + tuple(where[1:]))
        except:
            self.db.rollback()
            return 0
        self.db.commit()
        return 1
    
    def delete(self, table, where):
        query = "delete from %s where %s;" % \
            (table, where[0])
        try:
            self.db.execute(query, tuple(where[1:]))
        except:
            self.db.rollback()
            return 0
        self.db.commit()
        return 1
    
    def exists(self):
        pass

class Pins(BaseDatabaseObject):
    
    def __init__(self):
        super(Pins, self).__init__()
        self.data = {
            'pin_id': None,
            'image_url': None,
            'description': None,
            'refer_url': None,
            'updated': None
        }
    
    def save(self):
        self.data['updated'] = str(datetime.today())
        if self.exists():
            where = ['pin_id=?', self.data['pin_id']]
            return BaseDatabaseObject.update(self, 'pins', self.data, where)
        else:
            return BaseDatabaseObject.insert(self, 'pins', self.data)
    
    def exists(self):
        data = (self.data['pin_id'],)
        db = SQLite3().cursor()
        db.execute("select count(*) from pins where pin_id=?", data)
        return db.fetchone()[0]
    
    def size(self):
        res = self.db.execute('select count(*) from pins').fetchone()
        if res:
            return res[0]
        return 0
    
    def find_by_offset(self, offset):
        return self.db.execute('select * from pins limit ?, 1', (offset,)).fetchone()
    
    def get_candidates(self, offset=0, n=5, threshold=0.8):
        db = SQLite3().cursor()
        m = [r for r in db.execute('''
        select
            pins_a.pin_id,
            pins_a.image_url
        from
            clusters
        inner join
            pins pins_a on clusters.pin_id_a = pins_a.pin_id
        where
            clusters.score > ?
        order by clusters.score desc
        ''', (threshold,))]
        m = list(set(m))
        m.sort()
        m.reverse()
        return m[offset:offset+n]

class Words(BaseDatabaseObject):
    
    def __init__(self):
        super(Words, self).__init__()
        self.data = {
            'pin_id': None,
            'user': None,
            'word': None,
            'updated': None
        }
    
    def save(self):
        self.data['updated'] = str(datetime.today())
        if not self.exists():
            return BaseDatabaseObject.insert(self, 'words', self.data)
        else:
            # we don't update
            pass
    
    def delete(self):
        where = None
        if self.data['pin_id'] and self.data['user'] and self.data['word']:
            where = ['pin_id=? and user=? and word=?', \
                self.data['pin_id'], self.data['user'], self.data['word']]
        elif self.data['pin_id'] and self.data['user']:
            where = ['pin_id=? and user=?', \
                self.data['pin_id'], self.data['user']]
        elif self.data['pin_id']:
            where = ['pin_id=?', self.data['pin_id']]
        if not where:
            return
        return BaseDatabaseObject.delete(self, 'words', where)
    
    def exists(self):
        data = (self.data['pin_id'], self.data['user'], self.data['word'])
        db = SQLite3().cursor()
        db.execute("select count(*) from words where pin_id=? and user=? and word=?", data)
        return db.fetchone()[0]
    
    def set(self):
        # return list(set(words which are straged in database))
        res = self.db.execute('select word from words group by word').fetchall()
        if res:
            return res
        return []
    
    def find_by_pinid(self, pin_id):
        return self.db.execute('select word from words where pin_id = ?', (pin_id,)).fetchall()

class Clusters(BaseDatabaseObject):
    
    def __init__(self):
        super(Clusters, self).__init__()
        self.data = {
            'pin_id_a': None,
            'pin_id_b': None,
            'score': None,
            'updated': None
        }
    
    def save(self):
        self.data['updated'] = str(datetime.today())
        if self.exists():
            where = ['pin_id_a=? and pin_id_b=?', self.data['pin_id_a'], self.data['pin_id_b']]
            return BaseDatabaseObject.update(self, 'clusters', self.data, where)
        else:
            return BaseDatabaseObject.insert(self, 'clusters', self.data)
    
    def exists(self):
        data = (self.data['pin_id_a'], self.data['pin_id_b'])
        db = SQLite3().cursor()
        db.execute("select count(*) from clusters where pin_id_a=? and pin_id_b=?", data)
        return db.fetchone()[0]
    
    def get_top_matches(self, pin_id, n=5, threshold=0.8):
        q1 = '''
        select
            clusters.score,
            pins_a.image_url,
            pins_b.image_url,
            pins_b.pin_id
        from
            clusters
        inner join
            pins pins_a on clusters.pin_id_a = pins_a.pin_id
        inner join
            pins pins_b on clusters.pin_id_b = pins_b.pin_id
        where
            clusters.pin_id_a = ?
        AND clusters.score > ?
        order by clusters.score desc
        limit ?
        '''
        q2 = '''
        select
            clusters.score,
            pins_b.image_url,
            pins_a.image_url,
            pins_a.pin_id
        from
            clusters
        inner join
            pins pins_a on clusters.pin_id_a = pins_a.pin_id
        inner join
            pins pins_b on clusters.pin_id_b = pins_b.pin_id
        where
            clusters.pin_id_b = ?
        AND clusters.score > ?
        order by clusters.score desc
        limit ?
        '''
        db = SQLite3().cursor()
        m = [r for r in db.execute(q1, (pin_id, threshold, n))] +\
            [r for r in db.execute(q2, (pin_id, threshold, n))]
        m = list(set(m))
        m.sort()
        m.reverse()
        return m[:n]

def main():
    pass

if __name__ == '__main__': main()