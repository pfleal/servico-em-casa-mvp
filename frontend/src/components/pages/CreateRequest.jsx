import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth.jsx';
import { serviceAPI, requestAPI } from '../../lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Home as HomeIcon, 
  ArrowLeft, 
  MapPin, 
  DollarSign, 
  Calendar,
  AlertCircle,
  Loader2
} from 'lucide-react';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import './../../App.css';

const CreateRequest = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    category_id: '',
    title: '',
    description: '',
    address: user?.address || '',
    city: user?.city || '',
    state: user?.state || '',
    zip_code: user?.zip_code || '',
    urgency: 'normal',
    budget_min: '',
    budget_max: '',
    preferred_date: ''
  });

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const response = await serviceAPI.getCategories();
      setCategories(response.data.categories || []);
    } catch (error) {
      console.error('Erro ao carregar categorias:', error);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Validações
      if (!formData.category_id) {
        setError('Selecione uma categoria');
        return;
      }

      if (!formData.title.trim()) {
        setError('Título é obrigatório');
        return;
      }

      if (!formData.description.trim()) {
        setError('Descrição é obrigatória');
        return;
      }

      if (!formData.address.trim() || !formData.city.trim() || !formData.state.trim()) {
        setError('Endereço completo é obrigatório');
        return;
      }

      // Preparar dados para envio
      const requestData = {
        ...formData,
        category_id: parseInt(formData.category_id),
        budget_min: formData.budget_min ? parseFloat(formData.budget_min) : null,
        budget_max: formData.budget_max ? parseFloat(formData.budget_max) : null,
        preferred_date: formData.preferred_date || null
      };

      const response = await requestAPI.createRequest(requestData);
      
      if (response.data.request) {
        navigate(`/request/${response.data.request.id}`);
      }
    } catch (error) {
      setError(error.response?.data?.error || 'Erro ao criar pedido');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-card shadow-sm border-b">
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
            
            <div className="flex items-center">
              <ThemeToggle />
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Title */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Criar Novo Pedido
          </h2>
          <p className="text-gray-600">
            Descreva o serviço que você precisa e receba propostas de prestadores qualificados
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Detalhes do Serviço</CardTitle>
            <CardDescription>
              Preencha as informações abaixo para que os prestadores possam entender suas necessidades
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {/* Categoria */}
              <div className="space-y-2">
                <Label>Categoria do Serviço *</Label>
                <Select 
                  value={formData.category_id} 
                  onValueChange={(value) => handleChange('category_id', value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione uma categoria" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map((category) => (
                      <SelectItem key={category.id} value={category.id.toString()}>
                        {category.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Título */}
              <div className="space-y-2">
                <Label htmlFor="title">Título do Pedido *</Label>
                <Input
                  id="title"
                  placeholder="Ex: Instalação de chuveiro elétrico"
                  value={formData.title}
                  onChange={(e) => handleChange('title', e.target.value)}
                  required
                />
              </div>

              {/* Descrição */}
              <div className="space-y-2">
                <Label htmlFor="description">Descrição Detalhada *</Label>
                <Textarea
                  id="description"
                  placeholder="Descreva detalhadamente o serviço que você precisa, incluindo materiais necessários, prazo desejado e outras informações importantes..."
                  value={formData.description}
                  onChange={(e) => handleChange('description', e.target.value)}
                  rows={4}
                  required
                />
              </div>

              {/* Localização */}
              <div className="space-y-4">
                <div className="flex items-center">
                  <MapPin className="h-5 w-5 text-gray-400 mr-2" />
                  <Label className="text-lg font-medium">Localização</Label>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="address">Endereço *</Label>
                    <Input
                      id="address"
                      placeholder="Rua, número, bairro"
                      value={formData.address}
                      onChange={(e) => handleChange('address', e.target.value)}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="zip_code">CEP</Label>
                    <Input
                      id="zip_code"
                      placeholder="00000-000"
                      value={formData.zip_code}
                      onChange={(e) => handleChange('zip_code', e.target.value)}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="city">Cidade *</Label>
                    <Input
                      id="city"
                      placeholder="Sua cidade"
                      value={formData.city}
                      onChange={(e) => handleChange('city', e.target.value)}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="state">Estado *</Label>
                    <Input
                      id="state"
                      placeholder="SP"
                      value={formData.state}
                      onChange={(e) => handleChange('state', e.target.value)}
                      required
                    />
                  </div>
                </div>
              </div>

              {/* Urgência */}
              <div className="space-y-2">
                <Label>Urgência</Label>
                <Select 
                  value={formData.urgency} 
                  onValueChange={(value) => handleChange('urgency', value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Baixa - Posso esperar mais de uma semana</SelectItem>
                    <SelectItem value="normal">Normal - Até uma semana</SelectItem>
                    <SelectItem value="high">Alta - Até 3 dias</SelectItem>
                    <SelectItem value="urgent">Urgente - Hoje ou amanhã</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Orçamento */}
              <div className="space-y-4">
                <div className="flex items-center">
                  <DollarSign className="h-5 w-5 text-gray-400 mr-2" />
                  <Label className="text-lg font-medium">Orçamento (Opcional)</Label>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="budget_min">Valor Mínimo (R$)</Label>
                    <Input
                      id="budget_min"
                      type="number"
                      step="0.01"
                      placeholder="0,00"
                      value={formData.budget_min}
                      onChange={(e) => handleChange('budget_min', e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="budget_max">Valor Máximo (R$)</Label>
                    <Input
                      id="budget_max"
                      type="number"
                      step="0.01"
                      placeholder="0,00"
                      value={formData.budget_max}
                      onChange={(e) => handleChange('budget_max', e.target.value)}
                    />
                  </div>
                </div>
              </div>

              {/* Data Preferida */}
              <div className="space-y-2">
                <div className="flex items-center">
                  <Calendar className="h-5 w-5 text-gray-400 mr-2" />
                  <Label htmlFor="preferred_date">Data Preferida (Opcional)</Label>
                </div>
                <Input
                  id="preferred_date"
                  type="datetime-local"
                  value={formData.preferred_date}
                  onChange={(e) => handleChange('preferred_date', e.target.value)}
                />
              </div>

              {/* Botões */}
              <div className="flex justify-end space-x-4 pt-6">
                <Link to="/dashboard">
                  <Button variant="outline">Cancelar</Button>
                </Link>
                <Button type="submit" disabled={loading}>
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Criando...
                    </>
                  ) : (
                    'Criar Pedido'
                  )}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default CreateRequest;

