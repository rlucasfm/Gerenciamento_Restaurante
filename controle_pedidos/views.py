from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Produto, Pedido, ItensPedido


def Login(request):
    context ={}
    # Confirmação de usuário para o Navbar
    if request.user.is_authenticated:
        context['usuariologado'] = 'Logado como: ' + request.user.get_short_name()
        if (request.user.has_perm('controle_pedidos.delete_pedido')):
            return redirect(reverse('controle_pedidos:menu', ), context)
        else:
            return redirect(reverse('controle_pedidos:idcomanda', ), context)
    else:
        context['usuariologado'] = 'Deslogado'

    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if (request.user.has_perm('controle_pedidos.delete_pedido')):
                return redirect(reverse('controle_pedidos:menu', ), context)
            else:
                return redirect(reverse('controle_pedidos:idcomanda', ), context)

        else:
            context['erro'] = 'Usuário/Senha errada!'
            return render(request,'controle_pedidos/login.html', context)

    except(KeyError):
        return render(request, 'controle_pedidos/login.html', context)

def Logout(request):
    context = {}
    if request.user.is_authenticated:
        context['usuariologado'] = 'Logado como: ' + request.user.get_short_name()
    else:
        context['usuariologado'] = 'Deslogado'


    logout(request)
    return redirect(reverse('controle_pedidos:login', ), context)

def IDComanda(request):
    context = {}
    # Confirmação de usuário para o Navbar
    if request.user.is_authenticated:
        context['usuariologado'] = 'Logado como: ' + request.user.get_short_name()
        if (request.user.has_perm('controle_pedidos.delete_pedido')):
            context['perm']= True
            perm = True
        else:
            context['perm'] = False
            perm = False
    else:
        context['usuariologado'] = 'Deslogado'
        return redirect(reverse('controle_pedidos:login', ), context)

    try:
        idcomanda = request.POST['idcomanda']
        context['idpedido'] = int(idcomanda)
        try:
            #Se houver algum pedido com este código:
            if(Pedido.objects.filter(cod_comanda=idcomanda).count()!=0):
                if(perm):
                    return redirect(reverse('controle_pedidos:detalhespedidogerencia', args=(idcomanda,)),context)

                return redirect(reverse('controle_pedidos:detalhespedido', args=(idcomanda,)), context)

            #Se não houver pedido com este código
            else:
                context['erro'] = 'Não há comanda registrada com este ID!'
                if(perm):
                    context['perm'] = 'True'
                return render(request, 'controle_pedidos/idcomanda.html', context)
        except:
            return render(request, 'controle_pedidos/idcomanda.html', context)

    # Campo vazio, continuar na página
    except:
        return render(request, 'controle_pedidos/idcomanda.html', context)

def Menu(request):
    context = {}
    # Confirmação de usuário para o Navbar
    if request.user.is_authenticated:
        context['usuariologado'] = 'Logado como: ' + request.user.get_short_name()
        if (not request.user.has_perm('controle_pedidos.delete_pedido')):
            return redirect(reverse('controle_pedidos:idcomanda', ), context)
    else:
        context['usuariologado'] = 'Deslogado'
        return redirect(reverse('controle_pedidos:login', ), context)



    return render(request,'controle_pedidos/menu.html', context)

def DetalhesPedido(request, id):
    context = {}
    context['id'] = id


    # Confirmação de usuário para o Navbar
    if request.user.is_authenticated:
        context['usuariologado'] = 'Logado como: ' + request.user.get_short_name()
        if (request.user.has_perm('controle_pedidos.delete_pedido')):
            return redirect(reverse('controle_pedidos:menu', ), context)
    else:
        context['usuariologado'] = 'Deslogado'
        return redirect(reverse('controle_pedidos:login', ), context)

    # Listagem dos produtos para a tabela
    produtos = ItensPedido.objects.filter(cod_pedido=id)
    listaprodutos = []
    listavalores = []
    listaqnt = []
    for p in produtos:
        if(p.quantidade>0):
            listaprodutos.append(Produto.objects.get(pk=p.cod_produto).nome)
            listavalores.append(Produto.objects.get(pk=p.cod_produto).valor_unitario)
            listaqnt.append(p.quantidade)

    context['lista'] = tuple(zip(*(listaprodutos, listavalores, listaqnt)))

    valor_total = 0
    for indice, valor in enumerate(listavalores):
        valor_total+= valor*listaqnt[indice]

    Pedido.objects.filter(cod_comanda=id).update(valor_total=valor_total)
    context['valor_total'] = Pedido.objects.get(cod_comanda=id).valor_total

    listatodosprods = []

    for tp in Produto.objects.all():
        listatodosprods.append(tp)


    context['TodosProdutos'] = listatodosprods
    context['mesa'] = Pedido.objects.get(cod_comanda=id).cod_mesa
    context['pago'] = Pedido.objects.get(cod_comanda=id).pago
    # Receber/Deletar produtos adicionados
    try:
        nome_add = request.POST['selectprod']
        qnt_add = request.POST['qntprod']
        newprod = Produto.objects.get(nome=nome_add)
        qs = ItensPedido.objects.filter(cod_produto=newprod.pk).filter(cod_pedido=id)

        if(qs):
            index = 0
            for p in qs:
                if(index == 0):
                    qs.update(quantidade=p.quantidade+int(qnt_add))
                    index += 1
                    if(p.quantidade<=0):
                        p.delete()
                else:
                    p.delete()
            return redirect(reverse('controle_pedidos:detalhespedido', args=(id,)), context)
        else:
            ItensPedido(cod_pedido=id, cod_produto=newprod.pk, quantidade=qnt_add).save()
            return redirect(reverse('controle_pedidos:detalhespedido', args=(id,)), context)

    except(KeyError):
        return render(request, 'controle_pedidos/detalhespedido.html', context)

def NovoPedido(request, id):
    context = {}
    # Confirmação de usuário para o Navbar
    if request.user.is_authenticated:
        context['usuariologado'] = 'Logado como: ' + request.user.get_short_name()
        if (request.user.has_perm('controle_pedidos.delete_pedido')):
            return redirect(reverse('controle_pedidos:menu', ), context)
    else:
        context['usuariologado'] = 'Deslogado'
        return redirect(reverse('controle_pedidos:login', ), context)

    context['idcomanda'] = id

    try:
        codmesa = request.POST['codigomesa']
        Pedido(cod_comanda=id, cod_mesa=codmesa).save()
        return redirect(reverse('controle_pedidos:detalhespedido', args=(id,)), context)

    except(KeyError):
        return render(request, 'controle_pedidos/novopedido.html', context)

def DetalhesGerencia(request, id):
    context = {}
    context['id'] = id

    if request.user.is_authenticated:
        context['usuariologado'] = 'Logado como: ' + request.user.get_short_name()
        if (not request.user.has_perm('controle_pedidos.delete_pedido')):
            return redirect(reverse('controle_pedidos:idcomanda', ), context)
    else:
        context['usuariologado'] = 'Deslogado'
        return redirect(reverse('controle_pedidos:login', ), context)


    # Listagem dos produtos para a tabela
    produtos = ItensPedido.objects.filter(cod_pedido=id)
    listaprodutos = []
    listavalores = []
    listaqnt = []
    for p in produtos:
        if (p.quantidade > 0):
            listaprodutos.append(Produto.objects.get(pk=p.cod_produto).nome)
            listavalores.append(Produto.objects.get(pk=p.cod_produto).valor_unitario)
            listaqnt.append(p.quantidade)

    context['lista'] = tuple(zip(*(listaprodutos, listavalores, listaqnt)))

    listatodosprods = []

    for tp in Produto.objects.all():
        listatodosprods.append(tp)

    context['TodosProdutos'] = listatodosprods
    context['mesa'] = Pedido.objects.get(cod_comanda=id).cod_mesa
    context['pago'] = Pedido.objects.get(cod_comanda=id).pago

    try:
        statuspago = request.POST['pago']

        if(statuspago == 'Já foi feito'):
            Pedido.objects.filter(cod_comanda=id).update(pago=True)

        if(statuspago == 'Ainda não foi feito'):
            Pedido.objects.filter(cod_comanda=id).update(pago=False)

        context['pago'] = Pedido.objects.get(cod_comanda=id).pago
        return render(request, 'controle_pedidos/detalhesgerencia.html', context)

    except(KeyError):
        print('erro')
        return render(request, 'controle_pedidos/detalhesgerencia.html', context)

def GerenciaProdutos(request):
    context ={}

    # Confirmação de usuário para o Navbar
    if request.user.is_authenticated:
        context['usuariologado'] = 'Logado como: ' + request.user.get_short_name()
        if (not request.user.has_perm('controle_pedidos.delete_pedido')):
            return redirect(reverse('controle_pedidos:idcomanda', ), context)
    else:
        context['usuariologado'] = 'Deslogado'
        return redirect(reverse('controle_pedidos:login', ), context)

    context['listaprodutos'] = Produto.objects.all()


    return render(request, 'controle_pedidos/gerenciaprodutos.html', context)

def AdicionarProduto(request):
    context = {}

    # Confirmação de usuário para o Navbar
    if request.user.is_authenticated:
        context['usuariologado'] = 'Logado como: ' + request.user.get_short_name()
        if (not request.user.has_perm('controle_pedidos.delete_pedido')):
            return redirect(reverse('controle_pedidos:idcomanda', ), context)
    else:
        context['usuariologado'] = 'Deslogado'
        return redirect(reverse('controle_pedidos:login', ), context)

    try:
        nomeProd = request.POST['nomeProduto']
        valorProd = request.POST['valorProduto']
        descProd = request.POST['descricaoProduto']

        if(nomeProd and valorProd):
            Produto(nome=nomeProd,valor_unitario=valorProd).save()
            if(descProd):
                Produto(nome=nomeProd, valor_unitario=valorProd, descricao=descProd).save()
                return redirect(reverse('controle_pedidos:gerenciaprodutos',), context)
        else:
            context['erro']="Complete os campos de Nome e Valor do produto."
            return render(request, 'controle_pedidos/adicionarproduto.html', context)

    except(KeyError):
        return render(request, 'controle_pedidos/adicionarproduto.html', context)

    return render(request, 'controle_pedidos/adicionarproduto.html', context)

def DetalhesProduto(request,id):
    context ={}
    # Confirmação de usuário para o Navbar
    if request.user.is_authenticated:
        context['usuariologado'] = 'Logado como: ' + request.user.get_short_name()
        if (not request.user.has_perm('controle_pedidos.delete_pedido')):
            return redirect(reverse('controle_pedidos:idcomanda', ), context)
    else:
        context['usuariologado'] = 'Deslogado'
        return redirect(reverse('controle_pedidos:login', ), context)

    produto = Produto.objects.get(pk=id)
    context['nome'] = produto.nome
    context['valor'] = produto.valor_unitario
    context['descricao'] = produto.descricao

    try:
        nomeProd = request.POST['nomeProd']
        valorProd = request.POST['valorProd']
        descProd = request.POST['descProd']

        if(nomeProd and valorProd and descProd):
            Produto.objects.filter(pk=id).update(nome=nomeProd,valor_unitario=valorProd,descricao=descProd)
        if(nomeProd and valorProd and not descProd):
            Produto.objects.filter(pk=id).update(nome=nomeProd, valor_unitario=valorProd)
        if (nomeProd and descProd and not valorProd):
            Produto.objects.filter(pk=id).update(nome=nomeProd, descricao=descProd)
        if (valorProd and descProd and not nomeProd):
            Produto.objects.filter(pk=id).update(valor_unitario=valorProd, descricao=descProd)
        if (nomeProd and not valorProd and not descProd):
            Produto.objects.filter(pk=id).update(nome=nomeProd)
        if (not nomeProd and descProd and not valorProd):
            Produto.objects.filter(pk=id).update(descricao=descProd)
        if (valorProd and not descProd and not nomeProd):
            Produto.objects.filter(pk=id).update(valor_unitario=valorProd)

        # Repetir verificação após alteração
        produto = Produto.objects.get(pk=id)
        context['nome'] = produto.nome
        context['valor'] = produto.valor_unitario
        context['descricao'] = produto.descricao

        return render(request, 'controle_pedidos/detalhesproduto.html', context)

    except(KeyError):
        return render(request, 'controle_pedidos/detalhesproduto.html', context)

def ListaPedidos(request):
    context = {}
    # Confirmação de usuário para o Navbar
    if request.user.is_authenticated:
        context['usuariologado'] = 'Logado como: ' + request.user.get_short_name()
        if (not request.user.has_perm('controle_pedidos.delete_pedido')):
            return redirect(reverse('controle_pedidos:idcomanda', ), context)
    else:
        context['usuariologado'] = 'Deslogado'
        return redirect(reverse('controle_pedidos:login', ), context)

    try:
        idCom = request.POST['idCom']
        numMesa = request.POST['numMesa']
        dataCom = request.POST['dataCom']

        if(idCom and numMesa and dataCom):
            qs = Pedido.objects.filter(cod_comanda=idCom).filter(cod_mesa=numMesa).filter(data=dataCom)
        if (idCom and numMesa and not dataCom):
            qs = Pedido.objects.filter(cod_comanda=idCom).filter(cod_mesa=numMesa)
        if (idCom and not numMesa and dataCom):
            qs = Pedido.objects.filter(cod_comanda=idCom).filter(data=dataCom)
        if (not idCom and numMesa and dataCom):
            qs = Pedido.objects.filter(cod_mesa=numMesa).filter(data=dataCom)
        if (idCom and not numMesa and not dataCom):
            qs = Pedido.objects.filter(cod_comanda=idCom)
        if (not idCom and not numMesa and dataCom):
            qs = Pedido.objects.filter(data=dataCom)
        if (not idCom and numMesa and not dataCom):
            qs = Pedido.objects.filter(cod_mesa=numMesa)
        if (not idCom and not numMesa and not dataCom):
            qs = Pedido.objects.all()

        listaid = []
        listacod = []
        listadata = []
        listapago =[]
        listavalor =[]

        for prod in qs:
            listaid.append(Pedido.objects.get(pk=prod.pk).cod_comanda)
            listacod.append(Pedido.objects.get(pk=prod.pk).cod_mesa)
            listadata.append(Pedido.objects.get(pk=prod.pk).data)
            listavalor.append(Pedido.objects.get(pk=prod.pk).valor_total)
            if(Pedido.objects.get(pk=prod.pk).pago):
                listapago.append("Sim")
            else:
                listapago.append("Não")

        context['lista'] = tuple(zip(*(listaid, listacod, listadata, listapago, listavalor)))

        return render(request, 'controle_pedidos/listapedidos.html', context)

    except:
        return render(request, 'controle_pedidos/listapedidos.html', context)


