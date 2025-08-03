import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { serviceAPI } from '../../lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { 
  Search, 
  MapPin, 
  Star, 
  User,
  Filter,
  ArrowLeft
} from 'lucide-react';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import Logo from '../../assets/logo.svg';
import './../../App.css';

const SearchServices = () => {
  const [categories, setCategories] = useState([]);
  const [providers, setProviders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useState({
    category_id: '',
    city: '',
    state: '',
    keyword: '',
    min_rating: ''
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

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Filtrar parâmetros vazios
      const params = Object.fromEntries(
        Object.entries(searchParams).filter(([_, value]) => value !== '')
      );

      const response = await serviceAPI.searchProviders(params);
      setProviders(response.data.providers || []);
    } catch (error) {
      console.error('Erro na busca:', error);
      setProviders([]);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    // Converter "all" para string vazia para manter compatibilidade
    const processedValue = value === 'all' ? '' : value;
    setSearchParams(prev => ({
      ...prev,
      [field]: processedValue
    }));
  };

  const formatRating = (rating) => {
    return rating ? rating.toFixed(1) : '0.0';
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
                <img src={Logo} alt="Serviço em Casa" className="h-12 w-auto opacity-80" />
              </Link>
            </div>
            
            <div className="flex items-center">
              <ThemeToggle />
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Title */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Buscar Prestadores de Serviço
          </h2>
          <p className="text-gray-600">
            Encontre profissionais qualificados na sua região
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filtros */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Filter className="h-5 w-5 mr-2" />
                  Filtros de Busca
                </CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSearch} className="space-y-4">
                  {/* Palavra-chave */}
                  <div className="space-y-2">
                    <Label htmlFor="keyword">Palavra-chave</Label>
                    <Input
                      id="keyword"
                      placeholder="Ex: eletricista, limpeza..."
                      value={searchParams.keyword}
                      onChange={(e) => handleInputChange('keyword', e.target.value)}
                    />
                  </div>

                  {/* Categoria */}
                  <div className="space-y-2">
                    <Label>Categoria</Label>
                    <Select 
                      value={searchParams.category_id} 
                      onValueChange={(value) => handleInputChange('category_id', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Todas as categorias" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Todas as categorias</SelectItem>
                        {categories.map((category) => (
                          <SelectItem key={category.id} value={category.id.toString()}>
                            {category.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Cidade */}
                  <div className="space-y-2">
                    <Label htmlFor="city">Cidade</Label>
                    <Input
                      id="city"
                      placeholder="Ex: São Paulo"
                      value={searchParams.city}
                      onChange={(e) => handleInputChange('city', e.target.value)}
                    />
                  </div>

                  {/* Estado */}
                  <div className="space-y-2">
                    <Label htmlFor="state">Estado</Label>
                    <Input
                      id="state"
                      placeholder="Ex: SP"
                      value={searchParams.state}
                      onChange={(e) => handleInputChange('state', e.target.value)}
                    />
                  </div>

                  {/* Avaliação mínima */}
                  <div className="space-y-2">
                    <Label>Avaliação mínima</Label>
                    <Select 
                      value={searchParams.min_rating} 
                      onValueChange={(value) => handleInputChange('min_rating', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Qualquer avaliação" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Qualquer avaliação</SelectItem>
                        <SelectItem value="4">4+ estrelas</SelectItem>
                        <SelectItem value="3">3+ estrelas</SelectItem>
                        <SelectItem value="2">2+ estrelas</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <Button type="submit" className="w-full" disabled={loading}>
                    {loading ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Buscando...
                      </>
                    ) : (
                      <>
                        <Search className="h-4 w-4 mr-2" />
                        Buscar
                      </>
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Resultados */}
          <div className="lg:col-span-3">
            {providers.length === 0 && !loading ? (
              <Card>
                <CardContent className="text-center py-12">
                  <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Nenhum prestador encontrado
                  </h3>
                  <p className="text-gray-500">
                    Tente ajustar os filtros de busca ou expandir a área de procura.
                  </p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-medium text-gray-900">
                    {providers.length > 0 && `${providers.length} prestador${providers.length > 1 ? 'es' : ''} encontrado${providers.length > 1 ? 's' : ''}`}
                  </h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {providers.map((provider) => (
                    <Card key={provider.id} className="hover:shadow-md transition-shadow">
                      <CardHeader>
                        <div className="flex items-start justify-between">
                          <div className="flex items-center space-x-3">
                            <div className="bg-blue-100 rounded-full p-2">
                              <User className="h-6 w-6 text-blue-600" />
                            </div>
                            <div>
                              <CardTitle className="text-lg">{provider.name}</CardTitle>
                              <CardDescription className="flex items-center">
                                <MapPin className="h-4 w-4 mr-1" />
                                {provider.city}, {provider.state}
                              </CardDescription>
                            </div>
                          </div>
                          {provider.is_verified && (
                            <Badge variant="success">Verificado</Badge>
                          )}
                        </div>
                      </CardHeader>
                      <CardContent>
                        {provider.bio && (
                          <p className="text-gray-600 mb-4 line-clamp-2">
                            {provider.bio}
                          </p>
                        )}
                        
                        <div className="flex items-center justify-between mb-4">
                          <div className="flex items-center space-x-4">
                            <div className="flex items-center">
                              <Star className="h-4 w-4 text-yellow-400 mr-1" />
                              <span className="font-medium">{formatRating(provider.average_rating)}</span>
                            </div>
                            <div className="text-sm text-gray-500">
                              {provider.total_services} serviço{provider.total_services !== 1 ? 's' : ''}
                            </div>
                          </div>
                          
                          {provider.experience_years && (
                            <div className="text-sm text-gray-500">
                              {provider.experience_years} ano{provider.experience_years > 1 ? 's' : ''} de experiência
                            </div>
                          )}
                        </div>

                        <div className="flex justify-between items-center">
                          <div className="flex items-center">
                            {provider.is_available ? (
                              <Badge variant="success">Disponível</Badge>
                            ) : (
                              <Badge variant="secondary">Indisponível</Badge>
                            )}
                          </div>
                          
                          <div className="flex space-x-2">
                            <Button variant="outline" size="sm">
                              Ver Perfil
                            </Button>
                            <Button size="sm">
                              Contratar
                            </Button>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default SearchServices;

