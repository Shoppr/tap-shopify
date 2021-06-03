import shopify

from tap_shopify.context import Context
from tap_shopify.streams.base import Stream
from singer.utils import strftime, strptime_to_utc

from tap_shopify.streams.base import shopify_error_handling, RESULTS_PER_PAGE


class InventoryItem(Stream):
    name = 'inventory_items'
    replication_object = shopify.InventoryItem
    replication_key = 'updated_at'

    @shopify_error_handling
    def get_inventory_item(self, parent_object):
        ids = ','.join(
            [str(x.inventory_item_id) for x in parent_object.variants]
        )
        return self.replication_object.find(ids = ids, limit = RESULTS_PER_PAGE)

    def get_objects(self):
        selected_parent = Context.stream_objects['products']()
        selected_parent.name = 'products_inventory_items'

        for parent_object in selected_parent.get_objects():
            inventory_items = self.get_inventory_item(parent_object)

            for inventory_item in inventory_items:
                yield inventory_item

    def sync(self):
        bookmark = self.get_bookmark()
        max_bookmark = bookmark
        for inventory_item in self.get_objects():
            inventory_dict = inventory_item.to_dict()
            replication_value = strptime_to_utc(
                inventory_dict[self.replication_key]
            )

            if replication_value >= bookmark:
                yield inventory_dict

            if replication_value > max_bookmark:
                max_bookmark = replication_value

        self.update_bookmark(strftime(max_bookmark))


Context.stream_objects['inventory_items'] = InventoryItem
