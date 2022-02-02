from decimal import Decimal


from store.models import Product


class Basket():
    """
    A base Basket Class, providing some default behaviours that 
    can be inherited or overided, as necessary.
    """

    def __init__(self, request):
        
        self.session = request.session
        
        basket = self.session.get('skey')
        
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        
        self.basket = basket


    def add(self, product, product_qty, update=False):
        """Adding and updating the users basket session data

        Args:
            product ([type]): [description]
        """

        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty
        else:
            self.basket[product_id] = {
                'price':str(product.price),
                'qty':int(product_qty)
            }
        
        self.save()

    def save(self):
        self.session.modified = True
    
    def delete(self,product_id):
        """Delete item from session data

        Args:
            product_id ([type]): [description]
        """
        product_id = str(product_id)

        if product_id in self.basket:
            
            del self.basket[product_id]
        
        self.save()

    def update(self,product_id,qty):
        """Update values in session data

        Args:
            product_id ([type]): [description]
            qty ([type]): [description]
        """
        product_id = str(product_id)
        
        if product_id in self.basket.keys():
            self.basket[product_id]['qty'] = qty

        self.save()

    def __iter__(self):
        """to make this class iterable
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids) 
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
        Get the basket data and count the quantity of the items
        """

        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * int(item['qty']) for item in self.basket.values())