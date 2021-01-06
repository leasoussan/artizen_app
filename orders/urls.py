from django.urls import path
from .views import (
    MyOrders, 
    ConfrimItemOrderedDetail, 
    PaymentDetailCheckout, 
    InboxMessagesPanel, 
    SendMessageToBuyer, 
    OutboxMessagesPanel,
    SendMessageFromInbox,
    GuestOrderView,
    GuestMessage,
    ShowMessage,
    FinalConfirmationOrder,
    ReplayMessage
)

urlpatterns = [
    path('', MyOrders.as_view(), name = 'my_orders_board'),

    path('order_item/<int:pk>/', ConfrimItemOrderedDetail.as_view(), name = 'confirm_order_item'),

    path('payment_checkout/<int:pk>', PaymentDetailCheckout.as_view(), name = 'payment_checkout'),
    path('success_order/<int:pk>', FinalConfirmationOrder.as_view(), name = 'success_order_confirmation'),
    path('my_messages_panel/', InboxMessagesPanel.as_view(), name = 'my_messages_panel'),
    path('message/<int:pk>', ShowMessage.as_view(), name = 'message'),
    path('outbox_messages_panel/', OutboxMessagesPanel.as_view(), name = 'outbox_messages_panel'),
    path('replay_message/<int:pk>', ReplayMessage.as_view(), name = 'replay_message'),
    path('send_message/user/<int:pk>', SendMessageToBuyer.as_view(), name = 'send_message'),
    path('new_message/', SendMessageFromInbox.as_view(), name = 'new_message'),
    path('guest_get_order/<int:pk>', GuestOrderView.as_view(), name = 'guest_get_order'),
    path('guest_message_to_artist/<int:pk>', GuestMessage.as_view(), name = 'guest_message_to_artist'),
]
