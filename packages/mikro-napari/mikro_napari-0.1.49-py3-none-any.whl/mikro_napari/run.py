from arkitekt.apps.connected import ConnectedApp
from arkitekt.apps.fakts import ArkitektFakts
from arkitekt.apps.rekuest import ArkitektRekuest
from fakts.discovery.qt.selectable_beacon import (
    QtSelectableDiscovery,
    SelectBeaconWidget,
)
from fakts.fakts import Fakts
from fakts.grants.meta.failsafe import FailsafeGrant
from fakts.grants.remote.public_redirect_grant import PublicRedirectGrant
from fakts.grants.remote.claim import ClaimGrant
from herre.fakts.herre import FaktsHerre
from koil.composition.qt import QtPedanticKoil
from mikro_napari.widgets.main_widget import MikroNapariWidget

import napari
import argparse
from skimage.data import astronaut

from mikro_napari.widgets.sidebar.sidebar import SidebarWidget
import os

def main(**kwargs):

    os.environ["NAPARI_ASYNC"] = "1"

    viewer = napari.Viewer()

    app = ConnectedApp(
        rekuest=ArkitektRekuest(),
        fakts=ArkitektFakts(
            subapp="napari",
            grant=FailsafeGrant(
                grants=[
                    ClaimGrant(
                        client_id="go8CAE78FDf4eLsOSk4wkR4usYbsamcq0yTYqBiY",
                        client_secret="oO4eJgvv41Nkr9EaNAmZ5YI4WGgfJznUMW5ReGIcI6NsSXZiud3w3y2yGxdMf2WhEMdUKD6MMalLv1rlM8d6h5Q6vJR9vLbaKSHj2V5RpDrNVUWnJ1s2OmxiPSR6qoNH",
                        discovery=QtSelectableDiscovery(widget=SelectBeaconWidget(parent=viewer.window.qt_viewer)),
                    ),
                    PublicRedirectGrant(
                        name="Napari",
                        scopes=["openid"],
                        discovery=QtSelectableDiscovery(
                            widget=SelectBeaconWidget(parent=viewer.window.qt_viewer)
                        ),
                    ),
                ]
            ),
            assert_groups={"mikro", "rekuest"},
        ),
        herre=FaktsHerre(),
    )

    widget = MikroNapariWidget(viewer, app, **kwargs)
    sidebar = SidebarWidget(viewer, app, **kwargs)
    viewer.window.add_dock_widget(widget, area="left", name="Mikro")
    viewer.window.add_dock_widget(sidebar, area="right", name="Mikro")
    # viewer.add_image(astronaut(), name="astronaut")

    with app:
        napari.run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", help="Which config file to use", default="bergen.yaml", type=str
    )
    args = parser.parse_args()

    main(config_path=args.config)
