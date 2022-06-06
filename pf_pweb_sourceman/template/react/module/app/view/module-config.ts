import React from "react";
import PFLayoutInfoData from "@pfo/pf-react/src/artifacts/data/pf-layout-info-data";
import {_loadTranslation} from "@pfo/pf-pweb-i18n/app/pweb-i18n";
import PFURLMapping from "@pfo/pf-react/src/artifacts/config/pf-url-mapping";
import PFAppConfig from "@pfo/pf-react/src/artifacts/config/pf-app-config";
import {BANGLA} from "../locales/bn";
import {ENGLISH} from "../locales/en";


const IndexView = React.lazy(() => import('./index-view'));

const UI_BASE_URL = "/"
const API_BASE_URL = "api/v1/example/"

export default class __MODULE_NAME__Config {

    public static readonly API_URL = {
        LIST: API_BASE_URL + "list"
    }

    public static readonly uiURL = {
        index: UI_BASE_URL,
    }

    private static privateUrlMappings(privateLayoutInfo: PFLayoutInfoData): PFLayoutInfoData {
        return privateLayoutInfo;
    }

    private static publicUrlMappings(publicLayoutInfo: PFLayoutInfoData): PFLayoutInfoData {
        return publicLayoutInfo;
    }

    private static loadTranslation() {
        _loadTranslation("en", ENGLISH)
        _loadTranslation("bn", BANGLA)
    }

    public static register(urlMapping: PFURLMapping, appConfig: PFAppConfig): void {
        this.privateUrlMappings(urlMapping.privateLayout)
        this.publicUrlMappings(urlMapping.publicLayout)
        this.loadTranslation()
    }
}