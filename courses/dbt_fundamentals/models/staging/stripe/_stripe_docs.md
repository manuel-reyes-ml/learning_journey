{% docs payments_methods %}
    
One of the following values: 

| status         | definition                                       |
|----------------|--------------------------------------------------|
| credit_card         | Order placed, not yet shipped                    |
| bank_transfer        | Order has been shipped, not yet been delivered   |
| coupon      | Order has been received by customers             |
| gift_card | Customer indicated they want to return this item |

{% enddocs %}


{% docs payments_status %}
    
One of the following values: 

| status         | definition                                       |
|----------------|--------------------------------------------------|
| success        | Order placed, not yet shipped                    |
| fail        | Order has been shipped, not yet been delivered   |


{% enddocs %}