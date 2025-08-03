import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import { Search, Users, Star, Shield, Clock } from 'lucide-react';
import Logo from '../../assets/logo.svg';
import './../../App.css';

const Home = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-card shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <img src={Logo} alt="Serviço em Casa" className="h-16 w-auto mr-3" />
              <div className="flex flex-col">
                <h1 className="text-xl font-bold text-gray-900">Serviço em Casa</h1>
                <p className="text-sm text-gray-600">Tudo o que sua casa precisa, num só lugar.</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <ThemeToggle />
              <Link to="/login">
                <Button variant="ghost">Entrar</Button>
              </Link>
              <Link to="/register">
                <Button>Cadastrar-se</Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Conectamos você com os
            <span className="text-blue-600"> melhores prestadores</span>
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Encontre profissionais qualificados para serviços domésticos, reformas, limpeza e muito mais. 
            Rápido, seguro e confiável.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register">
              <Button size="lg" className="px-8 py-3 text-lg">
                Começar Agora
              </Button>
            </Link>
            <Link to="/search">
              <Button variant="outline" size="lg" className="px-8 py-3 text-lg">
                Buscar Serviços
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-card">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">
              Por que escolher o Serviço em Casa?
            </h3>
            <p className="text-lg text-gray-600">
              Oferecemos a melhor experiência para conectar clientes e prestadores
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center">
              <CardHeader>
                <Search className="h-12 w-12 text-blue-600 mx-auto mb-4" />
                <CardTitle>Busca Inteligente</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Encontre prestadores próximos a você com base na sua localização e necessidades específicas.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Shield className="h-12 w-12 text-green-600 mx-auto mb-4" />
                <CardTitle>Prestadores Verificados</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Todos os profissionais passam por verificação de documentos e histórico para sua segurança.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Star className="h-12 w-12 text-yellow-600 mx-auto mb-4" />
                <CardTitle>Sistema de Avaliações</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Avalie e seja avaliado. Construa sua reputação e escolha com base na experiência de outros.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-16 bg-muted">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">
              Como funciona
            </h3>
            <p className="text-lg text-gray-600">
              Em poucos passos você encontra o profissional ideal
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                1
              </div>
              <h4 className="text-lg font-semibold mb-2">Descreva seu Serviço</h4>
              <p className="text-gray-600">
                Conte-nos o que você precisa e onde você está localizado.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                2
              </div>
              <h4 className="text-lg font-semibold mb-2">Receba Propostas</h4>
              <p className="text-gray-600">
                Prestadores qualificados enviarão suas propostas com preços e prazos.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                3
              </div>
              <h4 className="text-lg font-semibold mb-2">Escolha o Melhor</h4>
              <p className="text-gray-600">
                Compare propostas, avaliações e escolha o profissional ideal.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                4
              </div>
              <h4 className="text-lg font-semibold mb-2">Avalie o Serviço</h4>
              <p className="text-gray-600">
                Após a conclusão, avalie o prestador e ajude outros usuários.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h3 className="text-3xl font-bold text-white mb-4">
            Pronto para encontrar o profissional ideal?
          </h3>
          <p className="text-xl text-blue-100 mb-8">
            Junte-se a milhares de usuários que já encontraram soluções para suas necessidades.
          </p>
          <Link to="/register">
            <Button size="lg" variant="secondary" className="px-8 py-3 text-lg">
              Criar Conta Gratuita
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center mb-4">
            <img src={Logo} alt="Serviço em Casa" className="h-8 w-8 mr-2" />
            <span className="text-lg font-semibold">Serviço em Casa</span>
          </div>
          <p className="text-gray-400">
            © 2025 Serviço em Casa. Conectando pessoas através de serviços de qualidade.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Home;

