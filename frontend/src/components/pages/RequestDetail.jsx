import { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth.jsx';
import { requestAPI, proposalAPI } from '../../lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Home as HomeIcon, 
  ArrowLeft, 
  MapPin, 
  Calendar, 
  DollarSign,
  User,
  Star,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import './../../App.css';

const RequestDetail = () => {
  const { id } = useParams();
  const { user } = useAuth();
  const [request, setRequest] = useState(null);
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadRequestDetail();
    if (user.user_type === 'client') {
      loadProposals();
    }
  }, [id, user.user_type]);

  const loadRequestDetail = async () => {
    try {
      const response = await requestAPI.getRequestDetail(id);
      setRequest(response.data.request);
    } catch (error) {
      setError('Erro ao carregar detalhes do pedido');
      console.error('Erro:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadProposals = async () => {
    try {
      const response = await proposalAPI.getProposalsByRequest(id);
      setProposals(response.data.proposals || []);
    } catch (error) {
      console.error('Erro ao carregar propostas:', error);
    }
  };

  const handleAcceptProposal = async (proposalId) => {
    try {
      await proposalAPI.acceptProposal(proposalId);
      loadRequestDetail();
      loadProposals();
    } catch (error) {
      setError('Erro ao aceitar proposta');
    }
  };

  const handleRejectProposal = async (proposalId) => {
    try {
      await proposalAPI.rejectProposal(proposalId);
      loadProposals();
    } catch (error) {
      setError('Erro ao rejeitar proposta');
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
    return new Date(dateString).toLocaleString('pt-BR');
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const getUrgencyLabel = (urgency) => {
    const urgencyMap = {
      low: 'Baixa',
      normal: 'Normal',
      high: 'Alta',
      urgent: 'Urgente'
    };
    return urgencyMap[urgency] || urgency;
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

  if (error || !request) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card>
          <CardContent className="text-center py-8">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {error || 'Pedido não encontrado'}
            </h3>
            <Link to="/dashboard">
              <Button>Voltar ao Dashboard</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Link to="/dashboard" className="mr-4">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Voltar
                </Button>
              </Link>
              <Link to="/" className="flex items-center">
                <HomeIcon className="h-8 w-8 text-blue-600 mr-2" />
                <h1 className="text-2xl font-bold text-gray-900">Serviço em Casa</h1>
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Detalhes do Pedido */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-2xl">{request.title}</CardTitle>
                    <CardDescription className="flex items-center mt-2">
                      <MapPin className="h-4 w-4 mr-1" />
                      {request.address}, {request.city}, {request.state}
                    </CardDescription>
                  </div>
                  {getStatusBadge(request.status)}
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">Descrição</h4>
                    <p className="text-gray-600">{request.description}</p>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <p className="text-sm text-gray-500">Urgência</p>
                      <p className="font-medium">{getUrgencyLabel(request.urgency)}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Criado em</p>
                      <p className="font-medium">{formatDate(request.created_at)}</p>
                    </div>
                    {request.budget_min && (
                      <div>
                        <p className="text-sm text-gray-500">Orçamento Mín.</p>
                        <p className="font-medium">{formatCurrency(request.budget_min)}</p>
                      </div>
                    )}
                    {request.budget_max && (
                      <div>
                        <p className="text-sm text-gray-500">Orçamento Máx.</p>
                        <p className="font-medium">{formatCurrency(request.budget_max)}</p>
                      </div>
                    )}
                  </div>

                  {request.preferred_date && (
                    <div>
                      <p className="text-sm text-gray-500">Data Preferida</p>
                      <p className="font-medium flex items-center">
                        <Calendar className="h-4 w-4 mr-1" />
                        {formatDate(request.preferred_date)}
                      </p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Informações do Cliente */}
            {request.client && (
              <Card>
                <CardHeader>
                  <CardTitle>Informações do Cliente</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center space-x-3">
                    <div className="bg-blue-100 rounded-full p-2">
                      <User className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <p className="font-medium">{request.client.name}</p>
                      <div className="flex items-center text-sm text-gray-500">
                        <Star className="h-4 w-4 mr-1 text-yellow-400" />
                        {request.client.average_rating?.toFixed(1) || '0.0'} 
                        ({request.client.total_services} serviços)
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Propostas */}
          <div className="space-y-6">
            {user.user_type === 'client' && (
              <Card>
                <CardHeader>
                  <CardTitle>Propostas Recebidas</CardTitle>
                  <CardDescription>
                    {proposals.length} proposta{proposals.length !== 1 ? 's' : ''} recebida{proposals.length !== 1 ? 's' : ''}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {proposals.length === 0 ? (
                    <p className="text-gray-500 text-center py-4">
                      Nenhuma proposta recebida ainda
                    </p>
                  ) : (
                    <div className="space-y-4">
                      {proposals.map((proposal) => (
                        <div key={proposal.id} className="border rounded-lg p-4">
                          <div className="flex justify-between items-start mb-3">
                            <div className="flex items-center space-x-2">
                              <div className="bg-gray-100 rounded-full p-1">
                                <User className="h-4 w-4 text-gray-600" />
                              </div>
                              <div>
                                <p className="font-medium">{proposal.provider.name}</p>
                                <div className="flex items-center text-sm text-gray-500">
                                  <Star className="h-3 w-3 mr-1 text-yellow-400" />
                                  {proposal.provider.average_rating?.toFixed(1) || '0.0'}
                                </div>
                              </div>
                            </div>
                            {getStatusBadge(proposal.status)}
                          </div>

                          <div className="space-y-2 mb-3">
                            <div className="flex justify-between">
                              <span className="text-sm text-gray-500">Valor:</span>
                              <span className="font-medium">{formatCurrency(proposal.price)}</span>
                            </div>
                            {proposal.estimated_duration && (
                              <div className="flex justify-between">
                                <span className="text-sm text-gray-500">Prazo:</span>
                                <span className="font-medium">{proposal.estimated_duration}</span>
                              </div>
                            )}
                            <div className="flex justify-between">
                              <span className="text-sm text-gray-500">Materiais:</span>
                              <span className="font-medium">
                                {proposal.materials_included ? 'Inclusos' : 'Não inclusos'}
                              </span>
                            </div>
                          </div>

                          {proposal.description && (
                            <p className="text-sm text-gray-600 mb-3">{proposal.description}</p>
                          )}

                          {proposal.status === 'pending' && request.status === 'open' && (
                            <div className="flex space-x-2">
                              <Button 
                                size="sm" 
                                onClick={() => handleAcceptProposal(proposal.id)}
                                className="flex-1"
                              >
                                <CheckCircle className="h-4 w-4 mr-1" />
                                Aceitar
                              </Button>
                              <Button 
                                variant="outline" 
                                size="sm" 
                                onClick={() => handleRejectProposal(proposal.id)}
                                className="flex-1"
                              >
                                Rejeitar
                              </Button>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Ações para Prestador */}
            {user.user_type === 'provider' && request.status === 'open' && (
              <Card>
                <CardHeader>
                  <CardTitle>Enviar Proposta</CardTitle>
                  <CardDescription>
                    Interessado neste serviço? Envie sua proposta!
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">
                    <DollarSign className="h-4 w-4 mr-2" />
                    Fazer Proposta
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default RequestDetail;

