from django.test import TestCase
from django.contrib.auth.models import User
from apps.perfil.models import Perfil, Endereco


class PerfilModelTestCase(TestCase):
    def setUp(self):
        # Criando um usuário para associar ao perfil
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            is_staff=True
        )
        self.client.login(username='adminuser', password='password123')

        self.perfil = Perfil.objects.create(
            usuario=self.user,
            avatar='contas/avatar/test.png',
            sexo=Perfil.Sexo.MASCULINO
        )

    def test_perfil_creation(self):
        """Testa se o perfil foi criado corretamente."""
        perfil = Perfil.objects.get(usuario=self.user)
        self.assertEqual(perfil.usuario.username, 'testuser')
        self.assertEqual(perfil.avatar, 'contas/avatar/test.png')
        self.assertEqual(perfil.sexo, Perfil.Sexo.MASCULINO)

    def test_perfil_str(self):
        """Testa o método __str__ do perfil."""
        perfil = Perfil.objects.get(usuario=self.user)
        self.assertEqual(str(perfil), f"{self.user.username} - Perfil")

    def test_perfil_update(self):
        """Testa a atualização de um perfil."""
        self.perfil.sexo = Perfil.Sexo.FEMININO
        self.perfil.save()
        perfil_atualizado = Perfil.objects.get(usuario=self.user)
        self.assertEqual(perfil_atualizado.sexo, Perfil.Sexo.FEMININO)

    def test_perfil_delete(self):
        """Testa a exclusão de um perfil."""
        self.perfil.delete()
        perfis = Perfil.objects.filter(usuario=self.user)
        self.assertEqual(perfis.count(), 0)


class EnderecoModelTestCase(TestCase):
    def setUp(self):
        # Criando um usuário e um perfil
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.perfil = Perfil.objects.create(
            usuario=self.user,
            avatar='contas/avatar/test.png',
            sexo=Perfil.Sexo.MASCULINO
        )
        self.endereco = Endereco.objects.create(
            perfil=self.perfil,
            rua='Rua Exemplo',
            numero='123',
            bairro='Centro',
            cidade='São Paulo',
            estado='SP',
            cep='12345-678',
            complemento='Apto 101'
        )

    def test_endereco_creation(self):
        """Testa se o endereço foi criado corretamente."""
        endereco = Endereco.objects.get(perfil=self.perfil)
        self.assertEqual(endereco.rua, 'Rua Exemplo')
        self.assertEqual(endereco.numero, '123')
        self.assertEqual(endereco.cidade, 'São Paulo')
        self.assertEqual(endereco.estado, 'SP')

    def test_endereco_str(self):
        """Testa o método __str__ do endereço."""
        endereco = Endereco.objects.get(perfil=self.perfil)
        self.assertEqual(str(endereco), 'Rua Exemplo, 123 - São Paulo/SP')

    def test_endereco_update(self):
        """Testa a atualização de um endereço."""
        self.endereco.cidade = 'Rio de Janeiro'
        self.endereco.estado = 'RJ'
        self.endereco.save()
        endereco_atualizado = Endereco.objects.get(perfil=self.perfil)
        self.assertEqual(endereco_atualizado.cidade, 'Rio de Janeiro')
        self.assertEqual(endereco_atualizado.estado, 'RJ')

    def test_endereco_delete(self):
        """Testa a exclusão de um endereço."""
        self.endereco.delete()
        enderecos = Endereco.objects.filter(perfil=self.perfil)
        self.assertEqual(enderecos.count(), 0)
