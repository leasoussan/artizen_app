from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from artists.views import ProfileCheckUserPassesTestMixin
from django.views import generic
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Order, MessageBox, PaymentDetail
from artists.models import Item
from artists.models import Profile
from django.urls import reverse_lazy
from .forms import CreateOrderForm, PaymentDetailsForm, SendMessageForm, NewMessageForm, GuestMessageForm, PaymentDetail
from termcolor import cprint
from accounts.mailers import send_message, guest_message_confirmation,  send_order_confirmation
from django.contrib import messages
from django.contrib.messages import get_messages


# ActiveUser ----------------------------LoginRequiredMixin, ProfileCheckUserPassesTestMixin---------------------

class MyOrders(LoginRequiredMixin, ProfileCheckUserPassesTestMixin, ListView):
    model = Order
    context_object_name = 'orders_list'
    template_name = 'orders/my_orders_dashboard.html'

    def get_queryset(self):
        orders = super().get_queryset().filter(item__artist__user =   self.request.user )

        return orders
        # what is the diff between these two?
      


class ConfrimItemOrderedDetail(LoginRequiredMixin, ProfileCheckUserPassesTestMixin, CreateView):
    model = Item
    form_class = CreateOrderForm
    template_name = 'orders/confirm_item_order.html'
    success_url = 'payment_checkout'

    def get_context_data(self, *args, **kwargs):
        item = Item.objects.get(pk=self.kwargs['pk'])  
        context = super().get_context_data(**kwargs)
        context['item'] = item
        return context    
    
    
    def get_success_url(self, pk):
        return redirect('payment_checkout', pk)


    def form_valid(self, form):
        order = form.save(commit = False)
        order.item = Item.objects.get(pk=self.kwargs['pk'])
        order.total_price = order.item.price * order.quantity
        order.buyer = self.request.user.profile
        order.save() 
        return self.get_success_url(pk=order.id)


class PaymentDetailCheckout(LoginRequiredMixin, ProfileCheckUserPassesTestMixin, CreateView):
    model = Order
    form_class = PaymentDetailsForm
    template_name = 'orders/checkout.html'
    success_url = 'success_order_confirmation'

    def get_context_data(self, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])  
        context = super().get_context_data(**kwargs)
        context['order'] = order
        cprint(order,'red')
        return context    


    def get_success_url(self, pk):
        return redirect('success_order_confirmation', pk)
    
    def form_valid(self, form):
        payment = form.save(commit = False)
        payment.order = Order.objects.get(pk=self.kwargs['pk'])
        payment.buyer = self.request.user.profile
        payment.save() 
        send_order_confirmation(payment)
        return self.get_success_url(pk=payment.id)



class  FinalConfirmationOrder(DetailView):
    model = PaymentDetail
    template_name = 'orders/success_order_confirmation.html'




#   _______________________Message      

class InboxMessagesPanel(LoginRequiredMixin, ProfileCheckUserPassesTestMixin, ListView):
    model = MessageBox
    context_object_name = 'messages_list'
    template_name = 'orders/box_messages.html'
    
    def get_queryset(self):
        inbox = super().get_queryset()
        return inbox.filter(receiver = self.request.user.profile)





class ShowMessage(DetailView):
    model = MessageBox
    template_name = 'orders/message.html' 



class OutboxMessagesPanel(LoginRequiredMixin, ProfileCheckUserPassesTestMixin, ListView):
    model = MessageBox
    context_object_name = 'outbox_message_list'
    template_name = 'orders/outbox_messages.html'

    def get_queryset(self):
        outbox = super().get_queryset()
        return outbox.filter(sender = self.request.user.profile)




class SendMessageToBuyer(LoginRequiredMixin, ProfileCheckUserPassesTestMixin, CreateView):
    model = MessageBox
    form_class = SendMessageForm
    template_name = 'orders/send_message.html'

    def get_context_data(self, *args, **kwargs):
        receiver = Profile.objects.get(pk=self.kwargs['pk']) 
        context = super().get_context_data(**kwargs)
        context['title'] = 'title'
        context['text'] = 'text'
        context['buyer'] = receiver 
    
    def form_valid(self, form):
        message = form.save(commit = False)
        buyer = Profile.objects.get(pk=self.kwargs['pk'])  
        message.receiver = buyer
        message.sender = self.request.user.profile
        message.save()
        send_message(message.receiver.user, message.subject, message.text)
        return super().form_valid(form)


class ReplayMessage(LoginRequiredMixin, ProfileCheckUserPassesTestMixin, CreateView):
    model = MessageBox
    form_class = SendMessageForm
    template_name = 'orders/message_replay.html'

    def get_context_data(self, *args, **kwargs):
        receiver = MessageBox.objects.get(pk=self.kwargs['pk']) 
        context = super().get_context_data(**kwargs)
        context['title'] = 'title'
        context['text'] = 'text'
        context['receiver'] = receiver
        return context    
    
    def form_valid(self, form):
        message = form.save(commit = False)
        to = message.receiver or message.email
        message.receiver = to
        message.sender = self.request.user.profile
        message.save()
    
        return super().form_valid(form)
        






class SendMessageFromInbox(LoginRequiredMixin, ProfileCheckUserPassesTestMixin, CreateView):
    model = MessageBox
    form_class = NewMessageForm
    template_name = 'orders/new_message.html'






class GuestOrderView(CreateView):
    model = Item
    template_name = 'artists/gestview_item.html'


class GuestMessage(CreateView):
    model = MessageBox
    form_class = GuestMessageForm
    template_name = 'orders/guest_message.html'


    def get_context_data(self, *args, **kwargs):
        receiver = Profile.objects.get(pk=self.kwargs['pk']) 
        context = super().get_context_data(**kwargs)
        context['subject'] = 'subject'
        context['text'] = 'text'
        context['receiver'] = receiver
        return context    
    
    def form_valid(self, form):
        message = form.save(commit = False)
        artist = Profile.objects.get(pk=self.kwargs['pk'])  
        message.receiver = artist
        message.email = self.request.POST.get('email')
        message.save()
        guest_message_confirmation(message)
        return super().form_valid(form)

