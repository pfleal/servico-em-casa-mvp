import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth.jsx';
import { requestAPI, proposalAPI } from '../../lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Plus, 
  Search, 
  User, 
  LogOut, 
  Clock, 
  CheckCircle, 
  XCircle,
  Star,
  MapPin,
  Calendar
} from 'lucide-react';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import Logo from '../../assets/logo.svg';
import './../../App.css';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [requests, setRequests] = useState([]);
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      if (user.user_type === 'client') {
        const requestsResponse = await requestAPI.getRequests();
        setRequests(requestsResponse.data.requests || []);
      } else {
        const proposalsResponse = await proposalAPI.getMyProposals();
        setProposals(proposalsResponse.data.proposals || []);
        
        const requestsResponse = await requestAPI.getRequests();
        setRequests(requestsResponse.data.requests || []);
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusMap = {
      open: { label: 'Aberto', variant: 'default' },
      in_progress: { label: 'Em Andamento', variant: 'secondary' },
      completed: { label: 'Concluído', variant: 'success' },
      cancelled: { label: 'Cancelado', variant: 'destructive' },
      pending: { label: 'Pendente', variant: 'default' },
      accepted: { label: 'Aceita', variant: 'success' },
      rejected: { label: 'Rejeitada', variant: 'destructive' }
    };
    
    const statusInfo = statusMap[status] || { label: status, variant: 'default' };
    return <Badge variant={statusInfo.variant}>{statusInfo.label}</Badge>;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Carregando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-card shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Link to="/" className="flex items-center">
                <img src={Logo} alt="Serviço em Casa" className="h-12 w-auto opacity-80" />
              </Link>
            </div>
            
            <div className="flex items-center space-x-4">
              <Link to="/search">
                <Button variant="outline" size="sm">
                  <Search className="h-4 w-4 mr-2" />
                  Buscar
                </Button>
              </Link>
              
              {user.user_type === 'client' && (
                <Link to="/create-request">
                  <Button size="sm">
                    <Plus className="h-4 w-4 mr-2" />
                    Novo Pedido
                  </Button>
                </Link>
              )}
              
              <Link to="/profile">
                <Button variant="ghost" size="sm">
                  <User className="h-4 w-4 mr-2" />
                  Perfil
                </Button>
              </Link>
              
              <ThemeToggle />
              
              <Button variant="ghost" size="sm" onClick={logout}>
                <LogOut className="h-4 w-4 mr-2" />
                Sair
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Olá, {user.name}!
          </h2>
          <p className="text-gray-600">
            {user.user_type === 'client' 
              ? 'Gerencie seus pedidos de serviço e encontre os melhores prestadores.'
              : 'Veja novos pedidos disponíveis e gerencie suas propostas.'
            }
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {user.user_type === 'client' ? 'Pedidos Ativos' : 'Propostas Enviadas'}
              </CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {user.user_type === 'client' 
                  ? requests.filter(r => r.status === 'open' || r.status === 'in_progress').length
                  : proposals.filter(p => p.status === 'pending').length
                }
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {user.user_type === 'client' ? 'Serviços Concluídos' : 'Propostas Aceitas'}
              </CardTitle>
              <CheckCircle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {user.user_type === 'client' 
                  ? requests.filter(r => r.status === 'completed').length
                  : proposals.filter(p => p.status === 'accepted').length
                }
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avaliação Média</CardTitle>
              <Star className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {user.average_rating ? user.average_rating.toFixed(1) : '0.0'}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Content Tabs */}
        <Tabs defaultValue={user.user_type === 'client' ? 'my-requests' : 'available-requests'} className="space-y-4">
          <TabsList>
            {user.user_type === 'client' ? (
              <>
                <TabsTrigger value="my-requests">Meus Pedidos</TabsTrigger>
              </>
            ) : (
              <>
                <TabsTrigger value="available-requests">Pedidos Disponíveis</TabsTrigger>
                <TabsTrigger value="my-proposals">Minhas Propostas</TabsTrigger>
              </>
            )}
          </TabsList>

          {/* Meus Pedidos (Cliente) */}
          {user.user_type === 'client' && (
            <TabsContent value="my-requests" className="space-y-4">
              {requests.length === 0 ? (
                <Card>
                  <CardContent className="text-center py-8">
                    <p className="text-gray-500 mb-4">Você ainda não criou nenhum pedido.</p>
                    <Link to="/create-request">
                      <Button>
                        <Plus className="h-4 w-4 mr-2" />
                        Criar Primeiro Pedido
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              ) : (
                requests.map((request) => (
                  <Card key={request.id}>
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-lg">{request.title}</CardTitle>
                          <CardDescription className="flex items-center mt-1">
                            <MapPin className="h-4 w-4 mr-1" />
                            {request.city}, {request.state}
                          </CardDescription>
                        </div>
                        {getStatusBadge(request.status)}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-gray-600 mb-4">{request.description}</p>
                      <div className="flex justify-between items-center">
                        <div className="flex items-center text-sm text-gray-500">
                          <Calendar className="h-4 w-4 mr-1" />
                          Criado em {formatDate(request.created_at)}
                        </div>
                        <Link to={`/request/${request.id}`}>
                          <Button variant="outline" size="sm">
                            Ver Detalhes
                          </Button>
                        </Link>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </TabsContent>
          )}

          {/* Pedidos Disponíveis (Prestador) */}
          {user.user_type === 'provider' && (
            <TabsContent value="available-requests" className="space-y-4">
              {requests.length === 0 ? (
                <Card>
                  <CardContent className="text-center py-8">
                    <p className="text-gray-500">Não há pedidos disponíveis no momento.</p>
                  </CardContent>
                </Card>
              ) : (
                requests.slice(0, 10).map((request) => (
                  <Card key={request.id}>
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-lg">{request.title}</CardTitle>
                          <CardDescription className="flex items-center mt-1">
                            <MapPin className="h-4 w-4 mr-1" />
                            {request.city}, {request.state}
                          </CardDescription>
                        </div>
                        {getStatusBadge(request.status)}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-gray-600 mb-4">{request.description}</p>
                      <div className="flex justify-between items-center">
                        <div className="flex items-center text-sm text-gray-500">
                          <Calendar className="h-4 w-4 mr-1" />
                          {formatDate(request.created_at)}
                        </div>
                        <Link to={`/request/${request.id}`}>
                          <Button size="sm">
                            Ver e Propor
                          </Button>
                        </Link>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </TabsContent>
          )}

          {/* Minhas Propostas (Prestador) */}
          {user.user_type === 'provider' && (
            <TabsContent value="my-proposals" className="space-y-4">
              {proposals.length === 0 ? (
                <Card>
                  <CardContent className="text-center py-8">
                    <p className="text-gray-500">Você ainda não enviou nenhuma proposta.</p>
                  </CardContent>
                </Card>
              ) : (
                proposals.map((proposal) => (
                  <Card key={proposal.id}>
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-lg">
                            {proposal.service_request?.title}
                          </CardTitle>
                          <CardDescription>
                            Cliente: {proposal.client?.name}
                          </CardDescription>
                        </div>
                        {getStatusBadge(proposal.status)}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-2 gap-4 mb-4">
                        <div>
                          <p className="text-sm text-gray-500">Valor Proposto</p>
                          <p className="font-semibold">{formatCurrency(proposal.price)}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Prazo Estimado</p>
                          <p className="font-semibold">{proposal.estimated_duration || 'Não informado'}</p>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <div className="flex items-center text-sm text-gray-500">
                          <Calendar className="h-4 w-4 mr-1" />
                          Enviada em {formatDate(proposal.created_at)}
                        </div>
                        <Link to={`/request/${proposal.service_request_id}`}>
                          <Button variant="outline" size="sm">
                            Ver Pedido
                          </Button>
                        </Link>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </TabsContent>
          )}
        </Tabs>
      </main>
    </div>
  );
};

export default Dashboard;

