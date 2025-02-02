from .models import session,User

class CRUD:
    def __init__(self,model):
        self.session = session
        self.model = model
    def add(self,**kwargs):
        try:
            obj=self.model(**kwargs)
            self.session.add(obj)
            self.session.commit()
            print("Successfully Added")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")

    def update(self,id_,**kwargs):
        try:
            obj=self.select_by_filter(id=id_)
            for k,v in kwargs.items():
                setattr(obj,k,v)
                self.session.commit()
                print("Successfully Updated")
        except Exception as e:
            print(e)

    def delete(self,**kwargs):

            obj=self.select_by_filter(**kwargs)
            self.session.delete(obj)
            self.session.commit()
            print('Successfully Deleted')


    def select_all(self):
        objects=self.session.query(self.model).all()
        return objects
    def select_column(self, column):
        # Use the column parameter in the query
        return self.session.query(column).all()
    def select_filter_all(self,**kwargs):
        objs=self.session.query(self.model).filter_by(**kwargs).all()
        return objs

    def select_by_filter(self,**kwargs):
        try:
            obj=self.session.query(self.model).filter_by(**kwargs).first()
            return obj
        except Exception as e:
            print(e)

    def select_with_max(self, column):
        """
        Ma'lum bir ustundagi maksimal qiymatga ega yozuvni qaytaradi.
        :param column: Maksimal qiymat qidiriladigan ustun (masalan: self.model.visit_count).
        """
        try:
            obj = (
                self.session.query(self.model)
                .order_by(column.desc())
                .first()
            )
            return obj
        except Exception as e:
            print(f"Error in select_with_max: {e}")
            return None

    def select_sorted_by_date(self):
        try:
            objects = self.session.query(self.model).order_by(self.model.created_at.desc()).all()
            return objects
        except Exception as e:
            print(e)
            return None


