import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react';

const CART_STORAGE_KEY = 'cart';

const CartContext = createContext(null);

const getStoredCart = () => {
  try {
    const storedCart = localStorage.getItem(CART_STORAGE_KEY);
    const parsedCart = storedCart ? JSON.parse(storedCart) : [];
    return Array.isArray(parsedCart) ? parsedCart : [];
  } catch {
    return [];
  }
};

export function CartProvider({ children }) {
  const [items, setItems] = useState(getStoredCart);

  useEffect(() => {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items));
  }, [items]);

  const addToCart = useCallback((product, quantity = 1) => {
    const requestedQuantity = Math.max(1, Number(quantity) || 1);
    const productId = Number(product.id);

    setItems((currentItems) => {
      const existingItem = currentItems.find(
        (item) => Number(item.id) === productId,
      );

      if (existingItem) {
        return currentItems.map((item) =>
          Number(item.id) === productId
            ? { ...item, quantity: item.quantity + requestedQuantity }
            : item,
        );
      }

      return [
        ...currentItems,
        {
          id: productId,
          name: product.name,
          image: product.image ?? null,
          price: Number(product.price) || 0,
          quantity: requestedQuantity,
        },
      ];
    });
  }, []);

  const updateQuantity = useCallback((productId, quantity) => {
    const nextQuantity = Math.max(1, Number(quantity) || 1);

    setItems((currentItems) =>
      currentItems.map((item) =>
        Number(item.id) === Number(productId)
          ? { ...item, quantity: nextQuantity }
          : item,
      ),
    );
  }, []);

  const removeFromCart = useCallback((productId) => {
    setItems((currentItems) =>
      currentItems.filter((item) => Number(item.id) !== Number(productId)),
    );
  }, []);

  const clearCart = useCallback(() => setItems([]), []);

  const { totalItems, provisionalTotal } = useMemo(
    () =>
      items.reduce(
        (totals, item) => {
          const quantity = Number(item.quantity) || 0;
          const price = Number(item.price) || 0;

          totals.totalItems += quantity;
          totals.provisionalTotal += quantity * price;
          return totals;
        },
        { totalItems: 0, provisionalTotal: 0 },
      ),
    [items],
  );

  const value = useMemo(
    () => ({
      items,
      addToCart,
      updateQuantity,
      removeFromCart,
      clearCart,
      totalItems,
      provisionalTotal,
    }),
    [
      items,
      addToCart,
      updateQuantity,
      removeFromCart,
      clearCart,
      totalItems,
      provisionalTotal,
    ],
  );

  return (
    <CartContext.Provider value={value}>{children}</CartContext.Provider>
  );
}

// oxlint-disable-next-line react/only-export-components
export function useCart() {
  const context = useContext(CartContext);

  if (!context) {
    throw new Error('useCart must be used inside CartProvider.');
  }

  return context;
}
