from arkitekt.apps.fakts import ArkitektFakts
from mikro_napari.widgets.main_widget import MikroNapariWidget
from arkitekt.apps.connected import ConnectedApp
from arkitekt.apps.rekuest import ArkitektRekuest
from fakts.fakts import Fakts
from fakts.grants.meta.failsafe import FailsafeGrant
from fakts.grants.remote.public_redirect_grant import PublicRedirectGrant
from herre.fakts.herre import FaktsHerre
from koil.composition.qt import QtPedanticKoil
from fakts.discovery.qt.selectable_beacon import (
    QtSelectableDiscovery,
    SelectBeaconWidget,
)
from fakts.grants.remote.claim import ClaimGrant


class ArkitektPluginWidget(MikroNapariWidget):
    def __init__(self, viewer: "napari.viewer.Viewer"):

        x = SelectBeaconWidget()

        app = ConnectedApp(
            koil=QtPedanticKoil(parent=self),
            rekuest=ArkitektRekuest(),
            fakts=ArkitektFakts(
                subapp="napari",
                grant=FailsafeGrant(
                    grants=[
                        ClaimGrant(
                            client_id="go8CAE78FDf4eLsOSk4wkR4usYbsamcq0yTYqBiY",
                            client_secret="oO4eJgvv41Nkr9EaNAmZ5YI4WGgfJznUMW5ReGIcI6NsSXZiud3w3y2yGxdMf2WhEMdUKD6MMalLv1rlM8d6h5Q6vJR9vLbaKSHj2V5RpDrNVUWnJ1s2OmxiPSR6qoNH",
                            discovery=QtSelectableDiscovery(widget=x),
                        ),
                        PublicRedirectGrant(
                            name="Napari",
                            scopes=["openid"],
                            discovery=QtSelectableDiscovery(widget=x),
                        ),
                    ]
                ),
                assert_groups={"mikro", "rekuest"},
            ),
            herre=FaktsHerre(),
        )

        super(ArkitektPluginWidget, self).__init__(viewer, app)

        app.enter()
