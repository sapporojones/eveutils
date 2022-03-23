from black import out
import requests


# if at work use proxies:
import os

os.environ["HTTP_PROXY"] = "http://proxy.jf.intel.com:911"
os.environ["HTTPS_PROXY"] = "http://proxy.jf.intel.com:912"


class EveUtils:
    def __init__(self):
        char_name: str = ""
        char_id: str = ""
        corp_id: str = ""
        alliance_id: str = ""
        system_id: str = ""
        system_name: str = ""
        item_id: str = ""
        item_name: str = ""
        region_id: str = ""
        type_id: str = ""
        system_jumps: int = 0

    def find_id_from_system(self, name):
        """
        Takes the name of a system and attempts to return the id
        :param name: The name of a system
        :return: the string value of the systemID
        """
        url_string = f"https://esi.evetech.net/latest/search/?categories=solar_system&datasource=tranquility&language=en-us&search={name}&strict=true"
        id_request = requests.get(url_string)
        id_request_json = id_request.json()
        system_id = id_request_json["solar_system"][0]
        self.system_id = str(system_id)
        return str(system_id)

    def find_system_from_id(self, id):
        """
        Returns system name from a provided id
        :param id:
        :return string containing name of a system:
        """
        url_string = f"https://esi.evetech.net/latest/universe/systems/{id}/?datasource=tranquility&language=en-us"
        id_request = requests.get(url_string)
        id_request_json = id_request.json()
        system_name = id_request_json["name"]
        self.system_name = system_name
        return system_name

    def get_jumps(self, sysid):
        """
        Retrieves number of jumps in the last 24h or whatever
        :param sysid: the integer value ID of the system to be checked
        :return: Returns integer number of jumps for specified system
        """
        base_url = "https://esi.evetech.net/latest/universe/system_jumps/?datasource=tranquility"
        ret_obj = requests.get(base_url)
        ret_json = ret_obj.json()
        for i in ret_json:
            if str(i["system_id"]) == str(sysid):
                sysjumps = i["ship_jumps"]
        self.system_jumps = sysjumps
        return sysjumps

    def get_character_id(self, character_name):
        """
        Takes the name of a character and attempts to determine and return the id of that character
        :param character_name: a string value representing the name of the corp
        :return: the id of the corporation in string form
        """
        char_srch = requests.get(
            f"https://esi.evetech.net/latest/search/?categories=character&datasource=tranquility"
            f"&language=en&search={character_name}&strict=true"
        )
        char_srch_json = char_srch.json()
        if len(char_srch_json) <= 0:
            raise Exception("Character not found")
        else:
            char_id = char_srch_json["character"][0]

        character_id = str(char_id)
        self.char_id = character_id
        return character_id

    def get_corp_id(self, corporation_name):
        """
        Takes a string value of a corporation name and attempts to determine and return the id of that corporation
        :param corporation_name: the string value of the name of the corp
        :return: the string representation of the id of the corp
        """
        corp_srch = requests.get(
            f"https://esi.evetech.net/latest/search/?categories=corporation&datasource=tranquility"
            f"&language=en&search={corporation_name}&strict=true"
        )
        corp_srch_json = corp_srch.json()
        if len(corp_srch_json) <= 0:
            raise Exception("Corporation not found")
        else:
            corp_id = str(corp_srch_json["corporation"][0])

        self.corp_id = corp_id
        return corp_id

    def get_alliance_id(self, alice_name):
        """
        Takes the name of an alliance and attempts to determine and return the id of that alliance
        :param alice_name: a string value representing the name of an alliance
        :return: a string representation of the id of the alliance
        """
        alice_srch = requests.get(
            f"https://esi.evetech.net/latest/search/?categories=alliance&datasource=tranquility"
            f"&language=en&search={alice_name}&strict=true"
        )
        alice_srch_json = alice_srch.json()
        if len(alice_srch_json) <= 0:
            raise Exception("Alliance not found")
        else:
            alice_id = str(alice_srch_json["alliance"][0])
        self.alliance_id = alice_id
        return alice_id

    def get_item_name(self, id):
        """
        Takes the id of an item and returns the name of that item
        :param id: the numeric item id to be passed to the api
        :return: a string representation of the name of the item
        """
        esi_route = f"https://esi.evetech.net/latest/universe/types/{id}/?datasource=tranquility&language=en"
        esi_resp = requests.get(esi_route)
        esi_json = esi_resp.json()
        name = str(esi_json["name"])
        self.item_name = name
        return name

    def get_region_id(self, sysid):
        """
        Given a systemid return the id of the region that contains it
        :param sysid:
        :return string containing the id of the region:
        """
        system_route = f"https://esi.evetech.net/latest/universe/systems/{sysid}/?datasource=tranquility&language=en"
        system_resp = requests.get(system_route)
        system_json = system_resp.json()
        const_id = system_json["constellation_id"]

        region_route = f"https://esi.evetech.net/latest/universe/constellations/{const_id}/?datasource=tranquility&language=en"
        region_resp = requests.get(region_route)
        region_json = region_resp.json()
        region_id = str(region_json["region_id"])
        self.region_id = region_id
        return region_id

    def get_item_id(self, item_name):
        """
        Returns the item id for a given item
        :param item_name:
        :return item_id:
        """
        item_id_get = requests.get(
            "https://esi.evetech.net/latest/search/",
            params={
                "categories": "inventory_type",
                "search": item_name,
                "strict": True,
            },
        )
        item_id_json = item_id_get.json()

        item_id = item_id_json["inventory_type"]

        out_item_id = str(item_id[0])
        self.item_id = out_item_id
        return out_item_id

    def num_stargates(self, sys_id):
        """
        Returns the number of stargates in a specified system.
        :param sys_id: System ID (int) of the designated system to lookup
        :return: integer value of the number of gates in a system.  Will always be >0
        """
        base_url = f"https://esi.evetech.net/latest/universe/systems/{sys_id}/"
        ret_obj = requests.get(base_url)
        obj_json = ret_obj.json()
        n_gates = len(obj_json["stargates"])
        return n_gates
