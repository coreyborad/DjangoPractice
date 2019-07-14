from populate import base
from order.models import Order, Order_item

def populate():
    print('Populating articles and comments ... ', end='')
    Order.objects.all().delete()
    Order_item.objects.all().delete()

    order = Order()
    order_item = Order_item()
    order.order_id = 'test'
    order_item.order_id = 'test2'
    order.save()
    order_item.save()
    # for title in titles:
    #     article = Article()
    #     article.title = title
    #     for j in range(20):
    #         article.content += title + '\n'
    #     article.save()
    #     for comment in comments:
    #         Comment.objects.create(article=article, content=comment)
    print('done')


if __name__ == '__main__':
    populate()