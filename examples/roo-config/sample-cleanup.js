// ============================================
// BEFORE CLEANUP - Messy JavaScript Code
// ============================================

var users = [];  // Global variable
const data = require('./data');  // Unused import

// Debug function
function debug(msg) {
    console.log('DEBUG: ' + msg);  // Debug output
}

function processOrder(order) {
    debug('Processing order: ' + order.id);
    // TODO: Add validation
    var total = 0;
    for (var i = 0; i < order.items.length; i++) {
        total = total + order.items[i].price * order.items[i].quantity;
    }
    console.log('Total: ' + total);  // Debug
    
    if (total > 0) {
        return {success: true, total: total};
    } else {
        return {success: false};
    }
}

// Duplicate logic!
function calculateTotal(items) {
    console.log('Calculating total...');  // Debug
    var sum = 0;
    for (var i = 0; i < items.length; i++) {
        sum = sum + items[i].price * items[i].quantity;
    }
    return sum;
}

class OrderManager {
    constructor() {
        this.orders = [];
    }
    
    add(o) {  // Poor naming
        console.log('Adding order');  // Debug
        this.orders.push(o);
    }
    
    remove(id) {
        // No error handling!
        var index = this.orders.findIndex(o => o.id == id);
        this.orders.splice(index, 1);
    }
    
    // Commented out old code
    // getOrder(id) {
    //     return this.orders.find(o => o.id == id);
    // }
}

// ============================================
// AFTER ROO CODE CLEANUP - Clean JavaScript
// ============================================

/**
 * Order processing module with comprehensive validation and error handling.
 * @module OrderProcessor
 */

/**
 * Represents an order item.
 * @typedef {Object} OrderItem
 * @property {number} price - Item price in cents
 * @property {number} quantity - Item quantity
 * @property {string} sku - Stock keeping unit identifier
 */

/**
 * Represents an order.
 * @typedef {Object} Order
 * @property {string} id - Unique order identifier
 * @property {OrderItem[]} items - Array of order items
 * @property {string} customerId - Customer identifier
 * @property {Date} createdAt - Order creation timestamp
 */

/**
 * Process an order and calculate the total amount.
 * 
 * @param {Order} order - The order to process
 * @returns {Promise<{success: boolean, total?: number, error?: string}>} Processing result
 * @throws {TypeError} If order is invalid or missing required fields
 * 
 * @example
 * const result = await processOrder({
 *   id: 'ORD-123',
 *   items: [{price: 1000, quantity: 2}],
 *   customerId: 'CUST-456'
 * });
 */
async function processOrder(order) {
    // Input validation
    if (!order || typeof order !== 'object') {
        throw new TypeError('Order must be a valid object');
    }
    
    if (!order.id || !order.items || !Array.isArray(order.items)) {
        throw new TypeError('Order must have id and items array');
    }
    
    if (order.items.length === 0) {
        return {
            success: false,
            error: 'Order must contain at least one item'
        };
    }
    
    try {
        // Calculate total using optimized method
        const total = order.items.reduce((sum, item) => {
            validateOrderItem(item);
            return sum + (item.price * item.quantity);
        }, 0);
        
        // Validate total amount
        if (total <= 0) {
            return {
                success: false,
                error: 'Order total must be greater than zero'
            };
        }
        
        // Log for production monitoring (not debug)
        if (process.env.NODE_ENV === 'production') {
            logger.info(`Order processed successfully`, {
                orderId: order.id,
                total,
                itemCount: order.items.length
            });
        }
        
        return {
            success: true,
            total
        };
        
    } catch (error) {
        logger.error(`Failed to process order ${order.id}:`, error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Validate an order item.
 * 
 * @param {OrderItem} item - The item to validate
 * @throws {Error} If item is invalid
 * @private
 */
function validateOrderItem(item) {
    if (!item || typeof item !== 'object') {
        throw new Error('Item must be a valid object');
    }
    
    if (typeof item.price !== 'number' || item.price < 0) {
        throw new Error('Item price must be a non-negative number');
    }
    
    if (typeof item.quantity !== 'number' || item.quantity <= 0) {
        throw new Error('Item quantity must be a positive number');
    }
}

/**
 * Manages a collection of orders with CRUD operations.
 * 
 * @class OrderManager
 * @example
 * const manager = new OrderManager();
 * await manager.addOrder(order);
 * const order = await manager.getOrder('ORD-123');
 */
class OrderManager {
    /**
     * Create a new OrderManager instance.
     */
    constructor() {
        /** @private {Map<string, Order>} */
        this.orders = new Map();
    }
    
    /**
     * Add a new order to the collection.
     * 
     * @param {Order} order - The order to add
     * @returns {Promise<void>}
     * @throws {Error} If order is invalid or already exists
     */
    async addOrder(order) {
        if (!order || !order.id) {
            throw new Error('Order must have a valid ID');
        }
        
        if (this.orders.has(order.id)) {
            throw new Error(`Order ${order.id} already exists`);
        }
        
        // Validate order before adding
        const validationResult = await processOrder(order);
        if (!validationResult.success) {
            throw new Error(`Invalid order: ${validationResult.error}`);
        }
        
        this.orders.set(order.id, {
            ...order,
            createdAt: order.createdAt || new Date()
        });
    }
    
    /**
     * Remove an order from the collection.
     * 
     * @param {string} orderId - The ID of the order to remove
     * @returns {boolean} True if order was removed, false if not found
     */
    removeOrder(orderId) {
        if (!orderId) {
            throw new Error('Order ID is required');
        }
        
        return this.orders.delete(orderId);
    }
    
    /**
     * Get an order by ID.
     * 
     * @param {string} orderId - The ID of the order to retrieve
     * @returns {Order|undefined} The order if found, undefined otherwise
     */
    getOrder(orderId) {
        if (!orderId) {
            throw new Error('Order ID is required');
        }
        
        return this.orders.get(orderId);
    }
    
    /**
     * Get all orders.
     * 
     * @returns {Order[]} Array of all orders
     */
    getAllOrders() {
        return Array.from(this.orders.values());
    }
    
    /**
     * Get the total number of orders.
     * 
     * @returns {number} The number of orders
     */
    getOrderCount() {
        return this.orders.size;
    }
}

// Export for use in other modules
module.exports = {
    processOrder,
    OrderManager
};