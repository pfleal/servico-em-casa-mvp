import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth.jsx';
import { authAPI, evaluationAPI } from '../../lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Home as HomeIcon, 
  ArrowLeft, 
  User, 
  Star, 
  Edit,
  Save,
  X,
  Phone,
  Mail,
  MapPin,
  Calendar
} from 'lucide-react';
import './../../App.css';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [evaluations, setEvaluations] = useState([]);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    phone: user?.phone || '',
    address: user?.address || '',
    city: user?.city || '',
    state: user?.state || '',
    zip_code: user?.zip_code || '',
    bio: user?.bio || '',
    experience_years: user?.experience_years || '',
    service_radius: user?.service_radius || '',
    is_available: user?.is_available || true
  });

  useEffect(() => {
    loadEvaluations();
  }, []);

  const loadEvaluations = async () => {
    try {
      const response = await evaluationAPI.getUserEvaluations(user.id);
      setEvaluations(response.data.evaluations || []);
    } catch (error) {
      console.error('Erro ao carregar avaliações:', error);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSave = async () => {
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const response = await authAPI.updateProfile(formData);
      updateUser(response.data.user);
      setSuccess('Perfil atualizado com sucesso!');
      setEditing(false);
    } catch (error) {
      setError(error.response?.data?.error || 'Erro ao atualizar perfil');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      name: user?.name || '',
      phone: user?.phone || '',
      address: user?.address || '',
      city: user?.city || '',
      state: user?.state || '',
      zip_code: user?.zip_code || '',
      bio: user?.bio || '',
      experience_years: user?.experience_years || '',
      service_radius: user?.service_radius || '',
      is_available: user?.is_available || true
    });
    setEditing(false);
    setError('');
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`h-4 w-4 ${i < rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`}
      />
    ));
  };

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

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Title */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Meu Perfil
          </h2>
          <p className="text-gray-600">
            Gerencie suas informações pessoais e configurações da conta
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Informações Principais */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <div className="flex justify-between items-center">
                  <div>
                    <CardTitle>Informações Pessoais</CardTitle>
                    <CardDescription>
                      Mantenha seus dados atualizados
                    </CardDescription>
                  </div>
                  {!editing ? (
                    <Button variant="outline" onClick={() => setEditing(true)}>
                      <Edit className="h-4 w-4 mr-2" />
                      Editar
                    </Button>
                  ) : (
                    <div className="flex space-x-2">
                      <Button size="sm" onClick={handleSave} disabled={loading}>
                        <Save className="h-4 w-4 mr-2" />
                        Salvar
                      </Button>
                      <Button variant="outline" size="sm" onClick={handleCancel}>
                        <X className="h-4 w-4 mr-2" />
                        Cancelar
                      </Button>
                    </div>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                {error && (
                  <Alert variant="destructive" className="mb-4">
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}
                
                {success && (
                  <Alert className="mb-4">
                    <AlertDescription>{success}</AlertDescription>
                  </Alert>
                )}

                <div className="space-y-4">
                  {/* Nome */}
                  <div className="space-y-2">
                    <Label htmlFor="name">Nome Completo</Label>
                    {editing ? (
                      <Input
                        id="name"
                        value={formData.name}
                        onChange={(e) => handleChange('name', e.target.value)}
                      />
                    ) : (
                      <p className="text-gray-900">{user?.name}</p>
                    )}
                  </div>

                  {/* E-mail (não editável) */}
                  <div className="space-y-2">
                    <Label>E-mail</Label>
                    <div className="flex items-center text-gray-600">
                      <Mail className="h-4 w-4 mr-2" />
                      {user?.email}
                    </div>
                  </div>

                  {/* Telefone */}
                  <div className="space-y-2">
                    <Label htmlFor="phone">Telefone</Label>
                    {editing ? (
                      <Input
                        id="phone"
                        value={formData.phone}
                        onChange={(e) => handleChange('phone', e.target.value)}
                      />
                    ) : (
                      <div className="flex items-center text-gray-900">
                        <Phone className="h-4 w-4 mr-2" />
                        {user?.phone || 'Não informado'}
                      </div>
                    )}
                  </div>

                  {/* Endereço */}
                  <div className="space-y-2">
                    <Label htmlFor="address">Endereço</Label>
                    {editing ? (
                      <Input
                        id="address"
                        value={formData.address}
                        onChange={(e) => handleChange('address', e.target.value)}
                      />
                    ) : (
                      <div className="flex items-center text-gray-900">
                        <MapPin className="h-4 w-4 mr-2" />
                        {user?.address || 'Não informado'}
                      </div>
                    )}
                  </div>

                  {/* Cidade e Estado */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="city">Cidade</Label>
                      {editing ? (
                        <Input
                          id="city"
                          value={formData.city}
                          onChange={(e) => handleChange('city', e.target.value)}
                        />
                      ) : (
                        <p className="text-gray-900">{user?.city || 'Não informado'}</p>
                      )}
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="state">Estado</Label>
                      {editing ? (
                        <Input
                          id="state"
                          value={formData.state}
                          onChange={(e) => handleChange('state', e.target.value)}
                        />
                      ) : (
                        <p className="text-gray-900">{user?.state || 'Não informado'}</p>
                      )}
                    </div>
                  </div>

                  {/* CEP */}
                  <div className="space-y-2">
                    <Label htmlFor="zip_code">CEP</Label>
                    {editing ? (
                      <Input
                        id="zip_code"
                        value={formData.zip_code}
                        onChange={(e) => handleChange('zip_code', e.target.value)}
                      />
                    ) : (
                      <p className="text-gray-900">{user?.zip_code || 'Não informado'}</p>
                    )}
                  </div>

                  {/* Campos específicos para prestadores */}
                  {user?.user_type === 'provider' && (
                    <>
                      <div className="space-y-2">
                        <Label htmlFor="bio">Biografia</Label>
                        {editing ? (
                          <Textarea
                            id="bio"
                            value={formData.bio}
                            onChange={(e) => handleChange('bio', e.target.value)}
                            rows={3}
                          />
                        ) : (
                          <p className="text-gray-900">{user?.bio || 'Não informado'}</p>
                        )}
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="experience_years">Anos de Experiência</Label>
                          {editing ? (
                            <Input
                              id="experience_years"
                              type="number"
                              value={formData.experience_years}
                              onChange={(e) => handleChange('experience_years', e.target.value)}
                            />
                          ) : (
                            <p className="text-gray-900">{user?.experience_years || 'Não informado'}</p>
                          )}
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="service_radius">Raio de Atendimento (km)</Label>
                          {editing ? (
                            <Input
                              id="service_radius"
                              type="number"
                              value={formData.service_radius}
                              onChange={(e) => handleChange('service_radius', e.target.value)}
                            />
                          ) : (
                            <p className="text-gray-900">{user?.service_radius || 'Não informado'}</p>
                          )}
                        </div>
                      </div>
                    </>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Estatísticas */}
            <Card>
              <CardHeader>
                <CardTitle>Estatísticas</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">Tipo de Conta</span>
                    <Badge variant={user?.user_type === 'provider' ? 'default' : 'secondary'}>
                      {user?.user_type === 'provider' ? 'Prestador' : 'Cliente'}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">Avaliação Média</span>
                    <div className="flex items-center">
                      <Star className="h-4 w-4 text-yellow-400 mr-1" />
                      <span className="font-medium">
                        {user?.average_rating?.toFixed(1) || '0.0'}
                      </span>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">Total de Serviços</span>
                    <span className="font-medium">{user?.total_services || 0}</span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">Membro desde</span>
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-1 text-gray-400" />
                      <span className="font-medium">
                        {user?.created_at ? formatDate(user.created_at) : 'N/A'}
                      </span>
                    </div>
                  </div>

                  {user?.user_type === 'provider' && (
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-500">Status</span>
                      <Badge variant={user?.is_available ? 'success' : 'secondary'}>
                        {user?.is_available ? 'Disponível' : 'Indisponível'}
                      </Badge>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Avaliações Recentes */}
            <Card>
              <CardHeader>
                <CardTitle>Avaliações Recentes</CardTitle>
                <CardDescription>
                  {evaluations.length} avaliação{evaluations.length !== 1 ? 'ões' : ''}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {evaluations.length === 0 ? (
                  <p className="text-gray-500 text-center py-4">
                    Nenhuma avaliação ainda
                  </p>
                ) : (
                  <div className="space-y-4">
                    {evaluations.slice(0, 3).map((evaluation) => (
                      <div key={evaluation.id} className="border-b pb-3 last:border-b-0">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center">
                            {renderStars(evaluation.rating)}
                          </div>
                          <span className="text-xs text-gray-500">
                            {formatDate(evaluation.created_at)}
                          </span>
                        </div>
                        {evaluation.comment && (
                          <p className="text-sm text-gray-600">{evaluation.comment}</p>
                        )}
                        <p className="text-xs text-gray-500 mt-1">
                          Por: {evaluation.evaluator.name}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Profile;

