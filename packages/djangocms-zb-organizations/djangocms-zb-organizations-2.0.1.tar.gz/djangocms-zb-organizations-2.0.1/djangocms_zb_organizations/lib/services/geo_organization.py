# -*- coding: utf-8 -*-

#  Copyright (C)  2022. CQ Inversiones SAS.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

# ****************************************************************
# IDE: PyCharm
# Developed by: JhonyAlexanderGonzal
# Date: 13/10/2022 2:25 p. m.
# Project: Djangocms-pruebas
# Module Name: geo_organization
# ****************************************************************
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from djangocms_zb_organizations.lib.exceptions import NotFound
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status, renderers
from rest_framework.exceptions import APIException
from rest_framework.exceptions import MethodNotAllowed

from djangocms_zb_organizations.lib.serializers import GeoOrganizationSerializer


@api_view(['POST'])
@renderer_classes([renderers.JSONRenderer])
def geo_json(request):
    try:
        data_return = []
        status_return = status.HTTP_400_BAD_REQUEST
        if request.is_ajax():
            if request.method == "POST" and request.data:
                ido = request.data
                queryset = GeoOrganizationSerializer.Meta.model.objects.get(organization=ido)
                serializer = GeoOrganizationSerializer(instance=queryset, many=False)
                data_return = serializer.data
                status_return = status.HTTP_200_OK if len(data_return) > 0 else status.HTTP_204_NO_CONTENT
        else:
            raise MethodNotAllowed("geo_json", detail=_("Request is not ajax"), code="not_ajax")
    except ObjectDoesNotExist as exc:
        raise NotFound(_("Organization polygon not found")) from exc
    except MethodNotAllowed as exc:
        raise MethodNotAllowed("geo_json", exc.detail, exc.get_codes()) from exc
    except Exception as exc:
        raise APIException(str(exc)) from exc
    else:
        return Response(data=data_return, status=status_return)
