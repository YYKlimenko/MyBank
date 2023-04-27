from rest_framework.permissions import IsAdminUser

from app.factories import CurrencyFactory, StockFactory
from app.services import AssetServiceProtocol
from app.views import AssetBaseView


class CurrencyView(AssetBaseView):
    """The view class for currencies."""
    _service: AssetServiceProtocol = CurrencyFactory.get_service()
    _category_name: str = 'currency'
    permission_classes = {'POST': IsAdminUser, 'PUT': IsAdminUser, 'DELETE': IsAdminUser}


class MoexStockView(AssetBaseView):
    """The view class for moex stocks."""
    _service: AssetServiceProtocol = StockFactory.get_service()
    _category_name: str = 'moex_stock'
    permission_classes = {'POST': IsAdminUser, 'PUT': IsAdminUser, 'DELETE': IsAdminUser}